package com.csc.recognization.pojo;

import org.springframework.beans.factory.annotation.Value;
import org.springframework.context.annotation.PropertySource;
import org.springframework.stereotype.Component;

import java.io.Serializable;

/**
 * 读取application.yaml中redis的配置信息
 */
@Component
@PropertySource({"classpath:application-common.properties"})
//@ConfigurationProperties(prefix = "spring.redis")
public class RedisConfigProperties implements Serializable {
    @Value("${spring.redis.host}")
    private String host;
    @Value("${spring.redis.port}")
    private Integer port;

    public RedisConfigProperties() {
    }

    public RedisConfigProperties(String host, Integer port) {
        this.host = host;
        this.port = port;
    }

    public String getHost() {
        return host;
    }

    public void setHost(String host) {
        this.host = host;
    }

    public Integer getPort() {
        return port;
    }

    public void setPort(Integer port) {
        this.port = port;
    }

    @Override
    public String toString() {
        return "RedisConfigProperties{" +
                "host='" + host + '\'' +
                ", port=" + port +
                '}';
    }
}
