package com.csc.classify;

import com.alibaba.dubbo.config.spring.context.annotation.EnableDubbo;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;

@SpringBootApplication
@EnableDubbo
public class ClassifyBackendApplication {

    public static void main(String[] args) {
        SpringApplication.run(ClassifyBackendApplication.class, args);
    }

}
