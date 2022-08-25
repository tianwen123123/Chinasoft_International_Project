package com.csc.recognization.pojo;


import java.io.Serializable;

public class User4Login implements Serializable {
    private String telephone;
    private String password;

    public User4Login() {
    }

    public User4Login(String telephone, String password) {
        this.telephone = telephone;
        this.password = password;
    }

    public String getTelephone() {
        return telephone;
    }

    public void setTelephone(String telephone) {
        this.telephone = telephone;
    }

    public String getPassword() {
        return password;
    }

    public void setPassword(String password) {
        this.password = password;
    }

    @Override
    public String toString() {
        return "User4Login{" +
                "telephone='" + telephone + '\'' +
                ", password='" + password + '\'' +
                '}';
    }
}

