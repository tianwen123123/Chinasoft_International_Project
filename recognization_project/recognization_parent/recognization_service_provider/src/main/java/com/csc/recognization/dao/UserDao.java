package com.csc.recognization.dao;

import com.csc.recognization.pojo.User4Login;
import com.csc.recognization.pojo.User4Register;
import org.apache.ibatis.annotations.Mapper;

@Mapper
public interface UserDao {
    //根据手机号查询用户
    public Integer findUserByTelephone(String telephone);

    //用户注册
    public void register(User4Register user4Register);

    //用户登录
    public Integer login(User4Login user4Login);
}
