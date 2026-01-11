package com.graf.use_grafana.modules.hello;

import io.micrometer.core.instrument.Counter;
import io.micrometer.core.instrument.MeterRegistry;
import io.micrometer.core.instrument.Timer;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequestMapping("/hello")
public class HelloController {

    private static final Logger logger = LoggerFactory.getLogger(HelloController.class);

    private final Counter logLinesCounter;
    private final Counter requestCounter;
    private final Timer requestTimer;

    @Autowired
    public HelloController(MeterRegistry meterRegistry, Counter logLinesCounter, Counter requestCounter) {
        this.logLinesCounter = logLinesCounter;
        this.requestCounter = requestCounter;
        this.requestTimer = Timer.builder("app.requests.latency")
                .description("Latency of HTTP requests")
                .register(meterRegistry);
    }

    @GetMapping
    public String hello() {
        return requestTimer.record(() -> {
            // Incrementar contador de peticiones
            requestCounter.increment();
            
            // Log de entrada de petición
            logWithCounter("Received GET request to /hello");
            
            // Simular procesamiento
            try {
                Thread.sleep((long) (Math.random() * 100));
            } catch (InterruptedException e) {
                Thread.currentThread().interrupt();
                logWithCounter("Thread interrupted: " + e.getMessage());
            }
            
            // Log de salida de petición
            logWithCounter("Responding to GET request to /hello");
            
            return "Hello from Spring Boot with Prometheus and Grafana!";
        });
    }

    private void logWithCounter(String message) {
        logger.info(message);
        logLinesCounter.increment();
    }
}