package com.csc.classify.service.impl;

import com.alibaba.dubbo.config.annotation.Service;
import com.alibaba.fastjson.JSON;
import com.alibaba.fastjson.JSONObject;
import com.csc.classfiy.service.PictureService;
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

@Service(interfaceClass = PictureService.class, timeout = 30000, retries = 0)
@Transactional
public class PictureServiceImpl implements PictureService {

    @Autowired
    private RestTemplate restTemplate;


    /**
     * 图片分类
     *
     * @param picName
     * @return
     */
    public Result classify(String picName) {
        String classify = null;
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
            classify = jsonObject.getString("classify_pic");
            licenselist = jsonObject.getObject("licenselist", java.util.List.class);
            System.out.println(classify);
            System.out.println(licenselist);
            if (licenselist == null || licenselist.size() == 0) {
                return new Result(false, MessageConstant.NOT_FIND_LICENSE);
            }
            int index = classify.indexOf("_");
            ret.add(classify.substring(index + 1));
            ret.add(licenselist);
            ret.add(classify.substring(0, index));

        } catch (RestClientException e) {
            e.printStackTrace();
            return new Result(false, MessageConstant.CLASSIFY_FAIL);
        }
        return new Result(true, MessageConstant.CLASSIFY_SUCCESS, ret);
    }
}
