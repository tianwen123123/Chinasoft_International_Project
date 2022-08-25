package com.csc.recognization.pojo;

import java.io.Serializable;

public class User4Register implements Serializable {

    private String nickname;
    private Integer gender;
    private String telephone;
    private String address;
    private String validate_code;
    private String password;
    private String reconfirm_password;

    public User4Register() {
    }

    public User4Register(String nickname, Integer gender, String telephone, String address, String validate_code, String password, String reconfirm_password) {
        this.nickname = nickname;
        this.gender = gender;
        this.telephone = telephone;
        this.address = address;
        this.validate_code = validate_code;
        this.password = password;
        this.reconfirm_password = reconfirm_password;
    }

    public String getNickname() {
        return nickname;
    }

    public void setNickname(String nickname) {
        this.nickname = nickname;
    }

    public Integer getGender() {
        return gender;
    }

    public void setGender(Integer gender) {
        this.gender = gender;
    }

    public String getTelephone() {
        return telephone;
    }

    public void setTelephone(String telephone) {
        this.telephone = telephone;
    }

    public String getAddress() {
        return address;
    }

    public void setAddress(String address) {
        this.address = address;
    }

    public String getValidate_code() {
        return validate_code;
    }

    public void setValidate_code(String validate_code) {
        this.validate_code = validate_code;
    }

    public String getPassword() {
        return password;
    }

    public void setPassword(String password) {
        this.password = password;
    }

    public String getReconfirm_password() {
        return reconfirm_password;
    }

    public void setReconfirm_password(String reconfirm_password) {
        this.reconfirm_password = reconfirm_password;
    }

    @Override
    public String toString() {
        return "User4Register{" +
                "nickname='" + nickname + '\'' +
                ", gender=" + gender +
                ", telephone='" + telephone + '\'' +
                ", address='" + address + '\'' +
                ", validate_code='" + validate_code + '\'' +
                ", password='" + password + '\'' +
                ", reconfirm_password='" + reconfirm_password + '\'' +
                '}';
    }
}
