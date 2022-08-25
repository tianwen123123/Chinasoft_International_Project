package com.csc.recognization.service;


import com.csc.recognization.pojo.User4Login;
import com.csc.recognization.pojo.User4Register;
import com.csc.recognization.result.Result;

public interface UserService {
    public Result register(User4Register user4Register);

    public Result sendValidateCode(String telephone);

    public Result login(User4Login user4Login);

}
