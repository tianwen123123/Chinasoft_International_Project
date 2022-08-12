package com.csc.classfiy.service;


import com.csc.classify.pojo.User4Register;
import com.csc.classify.result.Result;

public interface UserService {
    public Result register(User4Register user4Register);

    public Result sendValidateCode(String telephone);
}
