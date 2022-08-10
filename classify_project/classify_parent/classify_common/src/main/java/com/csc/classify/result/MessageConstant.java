package com.csc.classify.result;

import java.io.Serializable;

public class MessageConstant implements Serializable {
    //私有构造
    private MessageConstant() {
    }

    public static final String PIC_UPLOAD_FAIL = "图片上传失败";
    public static final String PIC_UPLOAD_SUCCESS = "图片上传成功";
    public static final String PIC_TIMEOUT = "图片过期了,请重新上传";
    public static final String CLASSIFY_SUCCESS = "图片分类成功";
    public static final String CLASSIFY_FAIL = "图片分类失败";
    public static final String REGISTER_SUCCESS = "注册成功";
    public static final String REGISTER_FAIL = "注册失败";
    public static final String TELEPHONE_WRONG = "手机号格式错误";
    public static final String NOT_NULL = "输入不能为空";
    public static final String TWICE_PASSWORD_NOT_EQUAL = "两次输入的密码不同";
    public static final String TELEPHONE_ALREADY_EXISTS = "手机号已经被注册";
    public static final String VALIDATE_CODE_WRONG = "验证码错误";
}
