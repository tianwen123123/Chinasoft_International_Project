package com.csc.recognization.result;

import java.io.Serializable;

public class MessageConstant implements Serializable {



    //私有构造
    private MessageConstant() {
    }

    public static final String PIC_UPLOAD_FAIL = "图片上传失败";
    public static final String PIC_UPLOAD_SUCCESS = "图片上传成功";
    public static final String PIC_TIMEOUT = "图片过期了,请重新上传";
    public static final String RECOGNIZE_SUCCESS = "检测成功";
    public static final String RECOGNIZE_FAIL = "检测失败";
    public static final String REGISTER_SUCCESS = "注册成功";
    public static final String REGISTER_FAIL = "注册失败";
    public static final String TELEPHONE_WRONG = "手机号格式错误";
    public static final String NOT_NULL = "输入不能为空";
    public static final String TWICE_PASSWORD_NOT_EQUAL = "两次输入的密码不同";
    public static final String TELEPHONE_ALREADY_EXISTS = "手机号已经被注册";
    public static final String VALIDATE_CODE_WRONG = "验证码错误";
    public static final String TELEPHONE_NOT_NULL = "手机号不能为空";
    public static final String SEND_SUCCESS = "验证码发送成功";
    public static final String SEND_FAIL = "验证码发送失败";
    public static final String LOGIN_FAIL = "登陆失败";
    public static final String LOGIN_SUCCESS = "登陆成功";
    public static final String USERNAME_OR_PASSWORD_WRONG = "手机或密码错误";
    public static final String VIDEO_NOT_NULL = "视频不能为空";
    public static final String VIDEO_FORMAT_WRONG = "视频格式错误";
    public static final String VIDEO_UPLOAD_FAIL = "视频上传失败";
    public static final String VIDEO_UPLOAD_SUCCESS = "视频上传成功";
    public static final String VIDEO_TIMEOUT = "视频超时";
    public static final String PROCESS_FAIL = "视频处理失败";
    public static final String PROCESS_SUCCESS = "视频处理成功";
    public static final String NOT_FIND_LICENSE = "未检测到车牌";
}
