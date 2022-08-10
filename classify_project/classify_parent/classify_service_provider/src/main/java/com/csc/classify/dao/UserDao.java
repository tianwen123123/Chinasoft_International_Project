package com.csc.classify.dao;

import com.csc.classify.pojo.User4Register;
import org.apache.ibatis.annotations.Mapper;

@Mapper
public interface UserDao {
    //根据手机号查询用户
    public Integer findUserByTelephone(String telephone);

    //用户注册
    public void register(User4Register user4Register);
}
