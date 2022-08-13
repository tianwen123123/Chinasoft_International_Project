package com.csc.classify.controller;

import com.alibaba.dubbo.config.annotation.Reference;
import com.csc.classfiy.service.VideoService;
import com.csc.classify.result.MessageConstant;
import com.csc.classify.result.Result;
import com.csc.classify.utils.QiniuUtils;
import com.csc.classify.utils.RedisUtils;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;
import org.springframework.web.multipart.MultipartFile;
import redis.clients.jedis.Jedis;

import java.io.File;
import java.io.IOException;
import java.util.UUID;

@RestController
public class VideoController {
    @Autowired
    private RedisUtils redisUtils;

    @Reference
    private VideoService videoService;

    @PostMapping("/video")
    public Result upload(@RequestParam("videoFile") MultipartFile videoFile) {
        if (videoFile == null)
            return new Result(false, MessageConstant.VIDEO_NOT_NULL);

        //获取原始字符串名称
        String originalName = videoFile.getOriginalFilename();
        //获取最后一个.的位置
        Integer index = originalName.lastIndexOf(".");
        //获取原始文件名的后缀
        String suffix = originalName.substring(index - 1);
        if (suffix != null && !suffix.trim().equals("") && (suffix.equals("mp4") || suffix.equals("mov") || suffix.equals("avi") || suffix.equals("wmv") || suffix.equals("m4v") || suffix.equals("dat") || suffix.equals("flv") || suffix.equals("mkv"))) {
            return new Result(false, MessageConstant.VIDEO_FORMAT_WRONG);
        }
        //设置新的文件名称
        String fileName = UUID.randomUUID() + suffix;

        //七牛云添加视频
        try {
            QiniuUtils.upload2Qiniu(videoFile.getBytes(), fileName);
        } catch (IOException e) {
            e.printStackTrace();
            return new Result(false, MessageConstant.VIDEO_UPLOAD_FAIL);
        }

        //向redis中添加视频名称
        //Todo:动态获取手机号
        Jedis jedis = redisUtils.getJedis();
        jedis.setex("18202275875/"+"video", 60 * 5, fileName);
        jedis.close();

        return new Result(true, MessageConstant.VIDEO_UPLOAD_SUCCESS, fileName);
    }

    @GetMapping("/video")
    public Result process(@RequestParam("telephone") String telephon){
        Jedis jedis = redisUtils.getJedis();
        //Todo:动态电话号码
        //jedis.get(telephone)
        String value = jedis.get("18202275875/video");
        if (value == null) {
            return new Result(false, MessageConstant.VIDEO_TIMEOUT);
        } else {
            try {
                videoService.process(value);
            } catch (Exception e) {
                e.printStackTrace();
                return new Result(false, MessageConstant.PROCESS_FAIL);
            }
        }

        //todo:换构造，还要返回classify结果
        return new Result(true,MessageConstant.PROCESS_SUCCESS);
    }
}