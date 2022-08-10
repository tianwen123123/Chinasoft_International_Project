package com.csc.classify.service.impl;

import com.alibaba.dubbo.config.annotation.Service;
import com.csc.classfiy.service.PictureService;
import org.springframework.transaction.annotation.Transactional;

@Service(interfaceClass = PictureService.class)
@Transactional
public class PictureServiceImpl implements PictureService {
    /**
     * 图片分类
     *
     * @param picName
     */
    public void classify(String picName) {
        //获取七牛云图片
        String path = "http://rgbvrgbry.hb-bkt.clouddn.com/"+picName;
        System.out.println(path);
        //与深度学习代码连接
        //TODO:深度学习连接
    }
}
