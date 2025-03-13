package com.example.jfrog.demo;import org.springframework.core.io.ClassPathResource;
import org.springframework.core.io.Resource;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;

public class Analysis {

    public void readFile(String filename) {
        Resource resource = new ClassPathResource(filename);
        try (InputStream is = resource.getInputStream();
             BufferedReader reader = new BufferedReader(new InputStreamReader(is))) {

            String line;
            while ((line = reader.readLine()) != null) {
                // 处理每一行
                System.out.println(line);
            }

        } catch (IOException e) {
            e.printStackTrace();
            // 处理异常，例如文件不存在或读取失败
        }
    }

    public static void main(String[] args) {
        Analysis reader = new Analysis();
        reader.readFile("artifactory-request.log"); // 假设文件在 src/main/resources/logs/logfile.log
    }
}

