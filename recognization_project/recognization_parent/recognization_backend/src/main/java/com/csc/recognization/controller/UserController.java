package com.csc.recognization.controller;

import com.alibaba.dubbo.config.annotation.Reference;
import com.csc.recognization.service.UserService;
import com.csc.recognization.pojo.User4Login;
import com.csc.recognization.pojo.User4Register;
import com.csc.recognization.result.MessageConstant;
import com.csc.recognization.result.Result;
import org.springframework.web.bind.annotation.*;

@RestController
public class UserController {

    @Reference
    private UserService userService;

    /**
     * 注册
     *
     * @param user4Register
     * @return
     */
    @PutMapping("/user")
    public Result register(@RequestBody User4Register user4Register) {
        //检验是否有空
        if (user4Register.getPassword() == null || user4Register.getPassword().trim().equals("") || user4Register.getReconfirm_password() == null || user4Register.getReconfirm_password().trim().equals("") || user4Register.getTelephone() == null || user4Register.getTelephone().trim().equals("") || user4Register.getValidate_code() == null || user4Register.getValidate_code().trim().equals(""))
            return new Result(false, MessageConstant.NOT_NULL);

        //检查手机号是否正确
        String telephone = user4Register.getTelephone();
        String reg = "^(13[0-9]|14[01456879]|15[0-35-9]|16[2567]|17[0-8]|18[0-9]|19[0-35-9])\\d{8}$";
        if (!telephone.matches(reg))
            return new Result(false, MessageConstant.TELEPHONE_WRONG);

        //正确则放行
        Result result = null;
        try {
            result = userService.register(user4Register);
        } catch (Exception e) {
            e.printStackTrace();
            return new Result(false, MessageConstant.REGISTER_FAIL);
        }

        return result;
    }

    /**
     * 发送验证码
     *
     * @param telephone
     * @return
     */
    @GetMapping("/user")
    public Result sendValidateCode(@RequestParam("telephone") String telephone) {
        //检验手机号是否正确
        if (telephone == null || telephone.trim().equals("")) {
            return new Result(false, MessageConstant.TELEPHONE_NOT_NULL);
        }
        String reg = "^(13[0-9]|14[01456879]|15[0-35-9]|16[2567]|17[0-8]|18[0-9]|19[0-35-9])\\d{8}$";
        if (!telephone.matches(reg)) {
            return new Result(false, MessageConstant.TELEPHONE_WRONG);
        }

        Result result = null;
        try {
            result = userService.sendValidateCode(telephone);
        } catch (Exception e) {
            e.printStackTrace();
            return new Result(false, MessageConstant.SEND_FAIL);
        }
        return result;
    }

    /**
     * 登录
     *
     * @return
     */
    @PostMapping("/user")
    public Result login(@RequestBody User4Login user4Login) {
        String telephone = user4Login.getTelephone();
        if (telephone == null || telephone.trim().equals("")) {
            return new Result(false, MessageConstant.TELEPHONE_NOT_NULL);
        }
        String reg = "^(13[0-9]|14[01456879]|15[0-35-9]|16[2567]|17[0-8]|18[0-9]|19[0-35-9])\\d{8}$";
        if (!telephone.matches(reg)) {
            return new Result(false, MessageConstant.TELEPHONE_WRONG);
        }

        Result result = null;
        try {
            result = userService.login(user4Login);
        } catch (Exception e) {
            e.printStackTrace();
            return new Result(false, MessageConstant.LOGIN_FAIL);
        }

        return result;
    }
}
