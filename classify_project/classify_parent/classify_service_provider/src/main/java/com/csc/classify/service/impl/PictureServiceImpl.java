package com.csc.classify.service.impl;

import com.alibaba.dubbo.config.annotation.Service;
import com.csc.classfiy.service.PictureService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpHeaders;
import org.springframework.http.ResponseEntity;
import org.springframework.transaction.annotation.Transactional;
import org.springframework.web.client.RestTemplate;

import java.util.HashMap;

@Service(interfaceClass = PictureService.class)
@Transactional
public class PictureServiceImpl implements PictureService {

    @Autowired
    private RestTemplate restTemplate;


    /**
     * 图片分类
     *
     * @param picName
     */
    public void classify(String picName) {
        //请求的url
        String url = "http://127.0.0.1:5000?pic=" + picName;

        //获取响应
        //若出现超时，则说明python部分处理时间过长，需要设置超时时间
        ResponseEntity<String> responseEntity = restTemplate.getForEntity(url, String.class);
        int statusCodeValue = responseEntity.getStatusCodeValue();
        HttpHeaders headers = responseEntity.getHeaders();
        String body = responseEntity.getBody();

        System.out.println("status:" + statusCodeValue);
        System.out.println("headers:" + headers);
        System.out.println("body:" + body);
    }
}
