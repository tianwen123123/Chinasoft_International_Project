package com.csc.classify.utils;

import com.tencentcloudapi.common.Credential;
import com.tencentcloudapi.common.exception.TencentCloudSDKException;
import com.tencentcloudapi.common.profile.ClientProfile;
import com.tencentcloudapi.common.profile.HttpProfile;
import com.tencentcloudapi.sms.v20210111.SmsClient;
import com.tencentcloudapi.sms.v20210111.models.*;
import org.apache.ibatis.io.Resources;

import java.io.IOException;
import java.io.Reader;
import java.util.Properties;

public class SMSUtils_Tencent {
    private static String secretId;
    private static String secretKey;
    private static String region;
    private static String[] phoneNumberSet;
    private static String smsSdkAppId;
    private static String templateId;
    private static String signName;
    private static String[] templateParamSet;

    static {
        Reader reader = null;
        Properties properties = null;
        try {
            reader = Resources.getResourceAsReader("SMS_Tencent.properties");
            properties = new Properties();
            properties.load(reader);
        } catch (IOException e) {
            e.printStackTrace();
        }
        //secretId
        secretId = properties.getProperty("secretId");
        //secretKey
        secretKey = properties.getProperty("secretKey");
        //region
        region = properties.getProperty("region");
        //phoneNumberSet
//        String phoneNumbers = properties.getProperty("phoneNumbers");
//        phoneNumberSet = phoneNumbers.split(",");
        //smsSdkAppId
        smsSdkAppId = properties.getProperty("smsSdkAppId");
        //templateId
        templateId = properties.getProperty("templateId");
        //signName
        signName = properties.getProperty("signName");
        //templateParam
//        String templateParam = properties.getProperty("templateParam");
//        templateParamSet = templateParam.split(",");
//        templateParamSet[0] = ValidateCodeUtils.generateValidateCode(6).toString();
    }

    public static void sendShortMessage(String[] phoneNumberSet,String validateCode) {
        String templateParam = validateCode+",5";
        String[] templateParamSet = templateParam.split(",");
        try {
            // 实例化一个认证对象，入参需要传入腾讯云账户secretId，secretKey,此处还需注意密钥对的保密
            // 密钥可前往https://console.cloud.tencent.com/cam/capi网站进行获取
            Credential cred = new Credential(secretId, secretKey);
            // 实例化一个http选项，可选的，没有特殊需求可以跳过
            HttpProfile httpProfile = new HttpProfile();
            httpProfile.setEndpoint("sms.tencentcloudapi.com");
            // 实例化一个client选项，可选的，没有特殊需求可以跳过
            ClientProfile clientProfile = new ClientProfile();
            clientProfile.setHttpProfile(httpProfile);
            // 实例化要请求产品的client对象,clientProfile是可选的
            SmsClient client = new SmsClient(cred, region, clientProfile);
            // 实例化一个请求对象,每个接口都会对应一个request对象
            SendSmsRequest req = new SendSmsRequest();
            req.setPhoneNumberSet(phoneNumberSet);

            req.setSmsSdkAppId(smsSdkAppId);
            req.setSignName(signName);
            req.setTemplateId(templateId);

            req.setTemplateParamSet(templateParamSet);
            // 返回的resp是一个SendSmsResponse的实例，与请求对象对应
            SendSmsResponse resp = client.SendSms(req);
            // 输出json格式的字符串回包
            System.out.println(SendSmsResponse.toJsonString(resp));
        } catch (TencentCloudSDKException e) {
            System.out.println(e.toString());
        }
    }
}
