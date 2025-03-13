package com.example.jfrog.demo;
import org.springframework.core.io.ClassPathResource;
import java.io.BufferedReader;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.util.ArrayList;
import java.util.List;
import java.util.stream.Collectors;

public class LogParser {

    public static void main(String[] args) throws Exception {
        // 如果你想用 ClassPathResource 读取日志文件，请确保该文件在类路径中
        String logFileName = "artifactory-request.log"; // 位于类路径中的文件名

        // 使用 ClassPathResource 读取文件
        ClassPathResource resource = new ClassPathResource(logFileName);

        if (!resource.exists()) {
            System.err.println("日志文件不存在: " + logFileName);
            System.exit(1);
        }

        // 解析文件
        LogParser parser = new LogParser();
        List<LogEntry> logEntries = parser.parseLogFile(resource);

        // 打印解析后的日志对象，方便调试
        logEntries.forEach(System.out::println);
    }

    public List<LogEntry> parseLogFile(ClassPathResource resource) {
        List<LogEntry> logEntries = new ArrayList<>();

        try (InputStream inputStream = resource.getInputStream();
             BufferedReader br = new BufferedReader(new InputStreamReader(inputStream))) {

            logEntries = br.lines().map(this::parseLogLine)
                    .filter(logEntry -> logEntry != null)
                    .collect(Collectors.toList());

        } catch (Exception e) {
            e.printStackTrace();
        }

        return logEntries;
    }

    private LogEntry parseLogLine(String line) {
        String[] fields = line.split("\\|");

        if (fields.length != 11) {
            System.err.println("无效的日志格式: " + line);
            return null;
        }

        try {
            String timestamp = fields[0];
            String requestId = fields[1];
            String clientIp = fields[2];
            String userEmail = fields[3];
            String httpMethod = fields[4];
            String requestUrl = fields[5];
            int responseCode = Integer.parseInt(fields[6]);
            long bytesUploaded = Long.parseLong(fields[7]);
            long bytesDownloaded = Long.parseLong(fields[8]);
            long duration = Long.parseLong(fields[9]);
            String userAgent = fields[10];

            return new LogEntry(timestamp, requestId, clientIp, userEmail, httpMethod, requestUrl,
                    responseCode, bytesUploaded, bytesDownloaded, duration, userAgent);
        } catch (Exception e) {
            System.err.println("解析日志行时出错: " + line);
            e.printStackTrace();
            return null;
        }
    }
}
