package com.csc.classify.classify_common;

import com.csc.classify.pojo.JedisPoolConfigProperties;
import com.csc.classify.pojo.RedisConfigProperties;
import com.csc.classify.utils.RedisUtils;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;
import redis.clients.jedis.Jedis;
import redis.clients.jedis.JedisPool;

import java.util.HashSet;

@SpringBootTest(classes = {JedisPoolConfigProperties.class,RedisConfigProperties.class,RedisUtils.class})
class ClassifyCommonApplicationTests {

    @Autowired
    private RedisConfigProperties redisConfigProperties;

    @Autowired
    private JedisPoolConfigProperties jedisPoolConfigProperties;

    @Autowired
    private RedisUtils redisUtils;

    @Test
    void testRedisConfig(){
        System.out.println(redisConfigProperties);
        System.out.println(jedisPoolConfigProperties);
    }

    @Test
    void testConRedis(){
        Jedis jedis = redisUtils.getJedis();
        jedis.close();
        /*HashSet<JedisPool> set = new HashSet<JedisPool>();
        for (int i = 0; i < 1000; i++) {
            Jedis jedis = redisUtils.getJedis();
            set.add(RedisUtils.jedisPool);
            jedis.close();
        }
        System.out.println(set.size());
        RedisUtils.jedisPool.close();*/
    }

}
