package com.csc.recognization.service.impl;

import com.alibaba.dubbo.config.annotation.Service;
import com.alibaba.fastjson.JSON;
import com.alibaba.fastjson.JSONObject;
import com.csc.recognization.service.PictureService;
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

@Service(interfaceClass = PictureService.class, timeout = 600000, retries = 0)
@Transactional
public class PictureServiceImpl implements PictureService {

    @Autowired
    private RestTemplate restTemplate;


    /**
     * 图片识别
     *
     * @param picName
     * @return
     */
    public Result recognize(String picName) {
        String recognization = null;
        List licenselist = null;
        ArrayList ret = new ArrayList<String>();
        try {
            //请求的url
            String url = "http://127.0.0.1:5000/pic?pic=" + picName;
            //获取响应
            //若出现超时，则说明python部分处理时间过长，需要设置超时时间
            ResponseEntity<String> responseEntity = restTemplate.getForEntity(url, String.class);
            int statusCodeValue = responseEntity.getStatusCodeValue();
            HttpHeaders headers = responseEntity.getHeaders();
            String body = responseEntity.getBody();

            JSONObject jsonObject = JSON.parseObject(body);
            recognization = jsonObject.getString("recognization_pic");
            licenselist = jsonObject.getObject("licenselist", java.util.List.class);
            if (licenselist == null || licenselist.size() == 0) {
                return new Result(false, MessageConstant.NOT_FIND_LICENSE);
            }
            int index = recognization.indexOf("_");
            ret.add(recognization.substring(index + 1));
            ret.add(licenselist);
            ret.add(recognization.substring(0, index));

        } catch (RestClientException e) {
            e.printStackTrace();
            return new Result(false, MessageConstant.RECOGNIZE_FAIL);
        }
        return new Result(true, MessageConstant.RECOGNIZE_SUCCESS, ret);
    }
}
