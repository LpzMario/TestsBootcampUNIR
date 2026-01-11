package com.graf.use_grafana;

import io.micrometer.core.instrument.Counter;
import io.micrometer.core.instrument.MeterRegistry;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.context.annotation.Bean;

@SpringBootApplication
public class UseGrafanaApplication {

    public static void main(String[] args) {
        SpringApplication.run(UseGrafanaApplication.class, args);
    }

    @Bean
    public Counter logLinesCounter(MeterRegistry meterRegistry) {
        return Counter.builder("app.log.lines")
                .description("Total number of log lines emitted by the application")
                .register(meterRegistry);
    }

    @Bean
    public Counter requestCounter(MeterRegistry meterRegistry) {
        return Counter.builder("app.requests.total")
                .description("Total number of requests processed")
                .register(meterRegistry);
    }
}