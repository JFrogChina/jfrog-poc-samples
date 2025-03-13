package com.example.jfrog.demo;
import javax.persistence.Entity;
import javax.persistence.GeneratedValue;
import javax.persistence.GenerationType;
import javax.persistence.Id;
import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.Setter;

@Entity
@Getter
@Setter
@NoArgsConstructor
public class LogEntry {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id; // 自动生成的主键

    private String timestamp;
    private String requestId;
    private String clientIp;
    private String userEmail;
    private String httpMethod;
    private String requestUrl;
    private int responseCode;
    private long bytesUploaded;
    private long bytesDownloaded;
    private long duration;
    private String userAgent;

    public LogEntry(String timestamp, String requestId, String clientIp, String userEmail,
                    String httpMethod, String requestUrl, int responseCode,
                    long bytesUploaded, long bytesDownloaded, long duration, String userAgent) {
        this.timestamp = timestamp;
        this.requestId = requestId;
        this.clientIp = clientIp;
        this.userEmail = userEmail;
        this.httpMethod = httpMethod;
        this.requestUrl = requestUrl;
        this.responseCode = responseCode;
        this.bytesUploaded = bytesUploaded;
        this.bytesDownloaded = bytesDownloaded;
        this.duration = duration;
        this.userAgent = userAgent;
    }
}

