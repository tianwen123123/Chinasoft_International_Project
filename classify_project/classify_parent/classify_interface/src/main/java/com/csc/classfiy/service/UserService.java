package com.csc.classfiy.service;


import com.csc.classify.pojo.User4Login;
import com.csc.classify.pojo.User4Register;
import com.csc.classify.result.Result;

public interface UserService {
    public Result register(User4Register user4Register);

    public Result sendValidateCode(String telephone);

    public Result login(User4Login user4Login);

}
