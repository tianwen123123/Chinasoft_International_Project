package com.csc.classify.service.impl;

import com.alibaba.dubbo.config.annotation.Service;
import com.csc.classfiy.service.VideoService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpHeaders;
import org.springframework.http.ResponseEntity;
import org.springframework.transaction.annotation.Transactional;
import org.springframework.web.client.RestTemplate;

@Service(interfaceClass = VideoService.class)
@Transactional
public class VideoServiceImpl implements VideoService {
    @Autowired
    private RestTemplate restTemplate;

    public void process(String videoName) {
        //请求的url
        String url = "http://127.0.0.1:5000?pic=" + videoName;

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
