package com.example.jfrog.demo.repository;
import com.example.jfrog.demo.LogEntry;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

@Repository
public interface LogEntryRepository extends JpaRepository<LogEntry, Long> {
    // 可以在这里定义自定义查询方法，例如按某些字段查询
}
