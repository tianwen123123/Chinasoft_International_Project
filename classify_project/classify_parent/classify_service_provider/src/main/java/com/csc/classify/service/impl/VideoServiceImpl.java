package com.csc.classify.service.impl;

import com.alibaba.dubbo.config.annotation.Service;
import com.alibaba.fastjson.JSON;
import com.alibaba.fastjson.JSONObject;
import com.csc.classfiy.service.VideoService;
import com.csc.classify.result.MessageConstant;
import com.csc.classify.result.Result;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpHeaders;
import org.springframework.http.ResponseEntity;
import org.springframework.transaction.annotation.Transactional;
import org.springframework.web.client.RestClientException;
import org.springframework.web.client.RestTemplate;

import java.util.ArrayList;
import java.util.List;

@Service(interfaceClass = VideoService.class)
@Transactional
public class VideoServiceImpl implements VideoService {
    @Autowired
    private RestTemplate restTemplate;

    public Result process(String videoName) {
        String classify = null;
        List licenselist = null;
        ArrayList ret = new ArrayList<String>();

        try {
            //请求的url
            String url = "http://127.0.0.1:5000?/video?video=" + videoName;
            //获取响应
            //若出现超时，则说明python部分处理时间过长，需要设置超时时间
            ResponseEntity<String> responseEntity = restTemplate.getForEntity(url, String.class);
            int statusCodeValue = responseEntity.getStatusCodeValue();
            HttpHeaders headers = responseEntity.getHeaders();
            String body = responseEntity.getBody();

            JSONObject jsonObject = JSON.parseObject(body);
            classify = jsonObject.getString("classify_pic");

            ret.add(classify);
        } catch (RestClientException e) {
            e.printStackTrace();
            return new Result(false, MessageConstant.CLASSIFY_FAIL);
        }
        return new Result(true, MessageConstant.CLASSIFY_SUCCESS, ret);
    }
}
