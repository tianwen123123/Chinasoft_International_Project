package com.csc.recognization.controller;


import com.alibaba.dubbo.config.annotation.Reference;
import com.csc.recognization.service.PictureService;
import com.csc.recognization.result.MessageConstant;
import com.csc.recognization.result.Result;
import com.csc.recognization.utils.QiniuUtils;
import com.csc.recognization.utils.RedisUtils;
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
    @Reference(timeout = 600000,retries = 0)
    private PictureService pictureService;

    /**
     * 上传图片
     *
     * @param imgFile
     * @return
     */
    @PostMapping("/picture")
    public Result upload(@RequestParam("imgFile") MultipartFile imgFile,@RequestParam("telephone") String telephone) {
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
        Jedis jedis = redisUtils.getJedis();
        jedis.setex(telephone+"/picture", 60 * 5, fileName);
        jedis.close();

        return new Result(true, MessageConstant.PIC_UPLOAD_SUCCESS, fileName);
    }

    /**
     * 图片识别
     *
     * @param telephone
     * @return
     */
    @GetMapping("/picture")
    public Result recognize(@RequestParam("telephone") String telephone) {
        Jedis jedis = redisUtils.getJedis();
        String value = jedis.get(telephone+"/picture");
        Result result = null;
        if (value == null) {
            return new Result(false, MessageConstant.PIC_TIMEOUT);
        } else {
            try {
                result = pictureService.recognize(value);
            } catch (Exception e) {
                e.printStackTrace();
                return new Result(false, MessageConstant.RECOGNIZE_FAIL);
            }
        }
        return result;
    }
}
