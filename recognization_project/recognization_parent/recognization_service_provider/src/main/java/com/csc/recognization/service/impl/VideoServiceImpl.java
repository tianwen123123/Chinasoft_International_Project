package com.csc.recognization.service.impl;

import com.alibaba.dubbo.config.annotation.Service;
import com.alibaba.fastjson.JSON;
import com.alibaba.fastjson.JSONObject;
import com.csc.recognization.service.VideoService;
import com.csc.recognization.result.MessageConstant;
import com.csc.recognization.result.Result;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpHeaders;
import org.springframework.http.ResponseEntity;
import org.springframework.transaction.annotation.Transactional;
import org.springframework.web.client.RestClientException;
import org.springframework.web.client.RestTemplate;

import java.util.ArrayList;
import java.util.List;

@Service(interfaceClass = VideoService.class, timeout = 600000, retries = 0)
@Transactional
public class VideoServiceImpl implements VideoService {
    @Autowired
    private RestTemplate restTemplate;

    public Result process(String videoName) {
        String locate_video = null;
        String locate_pic = null;
        List licenselist = null;
        ArrayList ret = new ArrayList<String>();

        try {
            //请求的url
            String url = "http://127.0.0.1:5000/video?video=" + videoName;
            //获取响应
            //若出现超时，则说明python部分处理时间过长，需要设置超时时间
            ResponseEntity<String> responseEntity = restTemplate.getForEntity(url, String.class);
            int statusCodeValue = responseEntity.getStatusCodeValue();
            HttpHeaders headers = responseEntity.getHeaders();
            String body = responseEntity.getBody();

            JSONObject jsonObject = JSON.parseObject(body);
            locate_video = jsonObject.getString("locate_video");
            locate_pic = jsonObject.getString("locate_pic");
            licenselist = jsonObject.getObject("licenselist", List.class);

            if (licenselist == null || licenselist.size() == 0) {
                return new Result(false, MessageConstant.NOT_FIND_LICENSE);
            }
            int index = locate_pic.indexOf("_");
            ret.add(locate_pic.substring(0, index));
            ret.add(locate_pic.substring(index + 1));
            ret.add(licenselist);
            ret.add(locate_video);
        } catch (RestClientException e) {
            e.printStackTrace();
            return new Result(false, MessageConstant.RECOGNIZE_FAIL);
        }
        return new Result(true, MessageConstant.RECOGNIZE_SUCCESS, ret);
    }
}
