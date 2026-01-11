package com.example.vaults3.controller;

import com.example.vaults3.service.S3Service;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.HashMap;
import java.util.List;
import java.util.Map;

@RestController
@RequestMapping("/api/s3")
public class S3Controller {

    private final S3Service s3Service;

    public S3Controller(S3Service s3Service) {
        this.s3Service = s3Service;
    }

    @GetMapping("/health")
    public ResponseEntity<Map<String, Object>> healthCheck() {
        Map<String, Object> response = new HashMap<>();
        boolean canAccess = s3Service.checkBucketAccess();
        
        response.put("status", canAccess ? "UP" : "DOWN");
        response.put("s3Access", canAccess);
        response.put("message", canAccess ? 
            "Successfully connected to S3 using Vault credentials" : 
            "Failed to connect to S3");
        
        return ResponseEntity.ok(response);
    }

    @GetMapping("/list")
    public ResponseEntity<List<String>> listObjects() {
        List<String> objects = s3Service.listObjects();
        return ResponseEntity.ok(objects);
    }

    @PostMapping("/upload")
    public ResponseEntity<String> uploadFile(
            @RequestParam String fileName,
            @RequestParam String content) {
        String result = s3Service.uploadFile(fileName, content);
        return ResponseEntity.ok(result);
    }
}