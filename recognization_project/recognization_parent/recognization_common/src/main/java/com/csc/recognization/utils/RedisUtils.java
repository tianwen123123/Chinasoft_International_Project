package com.csc.recognization.utils;

import com.csc.recognization.pojo.JedisPoolConfigProperties;
import com.csc.recognization.pojo.RedisConfigProperties;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Component;
import redis.clients.jedis.Jedis;
import redis.clients.jedis.JedisPool;
import redis.clients.jedis.JedisPoolConfig;

@Component
public class RedisUtils {
    private RedisUtils() {
    }

    private JedisPool jedisPool;

    @Autowired
    private JedisPoolConfigProperties jedisPoolConfigProperties;
    @Autowired
    private RedisConfigProperties redisConfigProperties;

    private JedisPoolConfig setJedisPoolConfig(){
        JedisPoolConfig jedisPoolConfig = new JedisPoolConfig();
        jedisPoolConfig.setTestOnBorrow(true);
        jedisPoolConfig.setTestOnReturn(true);
        jedisPoolConfig.setMaxTotal(jedisPoolConfigProperties.getMaxActive());
        jedisPoolConfig.setMaxIdle(jedisPoolConfigProperties.getMaxIdle());

        return jedisPoolConfig;
    }

    public Jedis getJedis(){
        //加锁，防止产生多个jedispool
        if(jedisPool==null){
            synchronized (this){
                if(jedisPool==null)
                    jedisPool = new JedisPool(setJedisPoolConfig(), redisConfigProperties.getHost(), redisConfigProperties.getPort(), 2000);

            }
        }
        return jedisPool.getResource();
    }

}
