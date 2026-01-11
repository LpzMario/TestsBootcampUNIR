package com.example.vaults3.service;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Service;
import software.amazon.awssdk.core.sync.RequestBody;
import software.amazon.awssdk.services.s3.S3Client;
import software.amazon.awssdk.services.s3.model.*;

import java.util.List;
import java.util.stream.Collectors;

@Service
public class S3Service {

    private static final Logger logger = LoggerFactory.getLogger(S3Service.class);

    private final S3Client s3Client;
    
    @Value("${aws.s3.bucket-name}")
    private String bucketName;

    public S3Service(S3Client s3Client) {
        this.s3Client = s3Client;
    }

    public List<String> listObjects() {
        try {
            logger.info("Listing objects in bucket: {}", bucketName);
            
            ListObjectsV2Request listRequest = ListObjectsV2Request.builder()
                    .bucket(bucketName)
                    .maxKeys(10)
                    .build();

            ListObjectsV2Response listResponse = s3Client.listObjectsV2(listRequest);
            
            List<String> objects = listResponse.contents().stream()
                    .map(S3Object::key)
                    .collect(Collectors.toList());
            
            logger.info("Found {} objects in bucket", objects.size());
            return objects;
            
        } catch (S3Exception e) {
            logger.error("Error listing S3 objects: {}", e.getMessage(), e);
            throw new RuntimeException("Failed to list S3 objects", e);
        }
    }

    public String uploadFile(String key, String content) {
        try {
            logger.info("Uploading file to S3: {}", key);
            
            PutObjectRequest putRequest = PutObjectRequest.builder()
                    .bucket(bucketName)
                    .key(key)
                    .build();

            s3Client.putObject(putRequest, RequestBody.fromString(content));
            
            logger.info("File uploaded successfully: {}", key);
            return "File uploaded successfully: " + key;
            
        } catch (S3Exception e) {
            logger.error("Error uploading file to S3: {}", e.getMessage(), e);
            throw new RuntimeException("Failed to upload file to S3", e);
        }
    }

    public boolean checkBucketAccess() {
        try {
            logger.info("Checking access to bucket: {}", bucketName);
            
            HeadBucketRequest headRequest = HeadBucketRequest.builder()
                    .bucket(bucketName)
                    .build();

            s3Client.headBucket(headRequest);
            
            logger.info("Successfully accessed bucket: {}", bucketName);
            return true;
            
        } catch (S3Exception e) {
            logger.error("Failed to access bucket: {}", e.getMessage());
            return false;
        }
    }
}