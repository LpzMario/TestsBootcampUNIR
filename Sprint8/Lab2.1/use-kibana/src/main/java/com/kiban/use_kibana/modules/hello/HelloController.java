package com.kiban.use_kibana.modules.hello;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

import java.time.LocalDateTime;

@RestController
@RequestMapping("/hello")
public class HelloController {

    private static final Logger logger = LoggerFactory.getLogger(HelloController.class);

    @GetMapping
    public String hello(@RequestParam(defaultValue = "World") String name) {
        logger.info("Endpoint /hello invocado con parámetro: {}", name);
        logger.info("Timestamp de la petición: {}", LocalDateTime.now());
        
        String response = "Hello, " + name + "!";
        logger.info("Respuesta generada: {}", response);
        
        return response;
    }

    @GetMapping("/error-test")
    public String errorTest() {
        logger.warn("Probando log de nivel WARNING");
        logger.error("Probando log de nivel ERROR para testing");
        return "Check logs for warning and error messages";
    }
}