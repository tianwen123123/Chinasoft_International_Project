package com.csc.classify.controller;


import com.alibaba.dubbo.config.annotation.Reference;
import com.csc.classfiy.service.PictureService;
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

import java.io.IOException;
import java.util.UUID;

@RestController
public class PictureController {
    //获取jedispool连接池
    @Autowired
    private RedisUtils redisUtils;
    //dubbo远程服务调用
    @Reference
    private PictureService pictureService;

    /**
     * 上传图片
     *
     * @param imgFile
     * @return
     */
    @PostMapping("/picture")
    public Result upload(@RequestParam("imgFile") MultipartFile imgFile) {
        //获取原始字符串名称
        String originalName = imgFile.getOriginalFilename();
        //获取最后一个.的位置
        Integer index = originalName.lastIndexOf(".");
        //获取原始文件名的后缀
        String suffix = originalName.substring(index - 1);
        //设置新的文件名称
        String fileName = UUID.randomUUID() + suffix;
        //七牛云添加图片
        try {
            QiniuUtils.upload2Qiniu(imgFile.getBytes(), fileName);
        } catch (IOException e) {
            e.printStackTrace();
            return new Result(false, MessageConstant.PIC_UPLOAD_FAIL);
        }

        //向redis中添加图片名称
        //Todo:动态获取手机号
        Jedis jedis = redisUtils.getJedis();
        jedis.setex("18202275875", 60 * 5, fileName);
        jedis.close();

        return new Result(true, MessageConstant.PIC_UPLOAD_SUCCESS, fileName);
    }

    /**
     * 图片分类
     *
     * @param telephone
     * @return
     */
    @GetMapping("/picture")
    public Result classify(@RequestParam("telephone") String telephone) {
        System.out.println(pictureService);
        Jedis jedis = redisUtils.getJedis();
        //Todo:动态电话号码
        //jedis.get(telephone)
        String value = jedis.get("18202275875");
        if (value == null) {
            return new Result(false, MessageConstant.PIC_TIMEOUT);
        } else {
            try {
                pictureService.classify(value);
            } catch (Exception e) {
                e.printStackTrace();
                return new Result(false, MessageConstant.CLASSIFY_FAIL);
            }
        }

        //todo:换构造，还要返回classify结果
        return new Result(true,MessageConstant.CLASSIFY_SUCCESS);
    }
}
