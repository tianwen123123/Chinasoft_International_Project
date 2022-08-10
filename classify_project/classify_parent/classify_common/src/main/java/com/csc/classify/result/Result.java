package com.csc.classify.result;

import java.io.Serializable;

public class Result implements Serializable {
    private Boolean flag;
    private String message;
    private Object data;

    //用于只返回成功/失败
    public Result(Boolean flag) {
        this.flag = flag;
    }

    //用于返回成功/失败与消息
    public Result(Boolean flag,String message){
        this.flag = flag;
        this.message = message;
    }

    //用于返回成功/失败、消息与数据
    public Result(Boolean flag,String message,Object data){
        this.flag = flag;
        this.message = message;
        this.data = data;
    }

    public Boolean getFlag() {
        return flag;
    }

    public void setFlag(Boolean flag) {
        this.flag = flag;
    }

    public String getMessage() {
        return message;
    }

    public void setMessage(String message) {
        this.message = message;
    }

    public Object getData() {
        return data;
    }

    public void setData(Object data) {
        this.data = data;
    }

    @Override
    public String toString() {
        return "Result{" +
                "flag=" + flag +
                ", message='" + message + '\'' +
                ", data=" + data +
                '}';
    }
}
