package com.csc.classify.service.impl;

import com.alibaba.dubbo.config.annotation.Service;
import com.csc.classfiy.service.UserService;
import com.csc.classify.dao.UserDao;
import com.csc.classify.pojo.User4Login;
import com.csc.classify.pojo.User4Register;
import com.csc.classify.result.MessageConstant;
import com.csc.classify.result.Result;
import com.csc.classify.utils.RedisUtils;
import com.csc.classify.utils.SMSUtils_Tencent;
import com.csc.classify.utils.ValidateCodeUtils;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.transaction.annotation.Transactional;
import redis.clients.jedis.Jedis;

@Service(interfaceClass = UserService.class)
@Transactional
public class UserServiceImpl implements UserService {

    @Autowired
    private UserDao userDao;

    @Autowired
    private RedisUtils redisUtils;

    /**
     * 注册
     *
     * @param user4Register
     * @return
     */
    public Result register(User4Register user4Register) {
        //1.先查询手机号是否被注册过
        String telephone = user4Register.getTelephone();
        Integer id = userDao.findUserByTelephone(telephone);
        if (id != null)
            return new Result(false, MessageConstant.TELEPHONE_ALREADY_EXISTS);

        //2.检查验证码是否正确
        Jedis jedis = redisUtils.getJedis();
        String validate_code_in_redis = jedis.get(telephone);
        String validate_code = user4Register.getValidate_code();
        jedis.close();
        if (!validate_code.equals(validate_code_in_redis))
            return new Result(false, MessageConstant.VALIDATE_CODE_WRONG);

        //3.判断两次密码是否相同
        String password = user4Register.getPassword();
        String reconfirm_password = user4Register.getReconfirm_password();
        if (!password.equals(reconfirm_password))
            return new Result(false, MessageConstant.TWICE_PASSWORD_NOT_EQUAL);

        //4.注册
        userDao.register(user4Register);
        return new Result(true, MessageConstant.REGISTER_SUCCESS);
    }

    /**
     * 发送验证码
     *
     * @param telephone
     * @return
     */
    public Result sendValidateCode(String telephone) {
        Jedis jedis = null;
        try {

            Integer valCode = ValidateCodeUtils.generateValidateCode(6);
            SMSUtils_Tencent.sendShortMessage(new String[]{telephone}, valCode.toString());
            //存入redis里
            jedis = redisUtils.getJedis();
            jedis.setex(telephone, 300, valCode.toString());

            return new Result(true, MessageConstant.SEND_SUCCESS);
        } catch (Exception e) {
            e.printStackTrace();
            return new Result(false, MessageConstant.SEND_FAIL);
        } finally {
            if (jedis != null)
                jedis.close();
        }
    }


    public Result login(User4Login user4Login) {
        Integer id = userDao.login(user4Login);
        if (id != null)
            return new Result(true, MessageConstant.LOGIN_SUCCESS);
        else
            return new Result(false,MessageConstant.USERNAME_OR_PASSWORD_WRONG);
    }
}
