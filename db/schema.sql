#创建数据库和表
CREATE DATABASE IF NOT EXISTS server_monitor;
USE server_monitor;

CREATE TABLE IF NOT EXISTS monitor_log (
    id INT AUTO_INCREMENT PRIMARY KEY,
    timestamp DATETIME,
    cpu_percent FLOAT,
    memory_percent FLOAT,
    disk_percent FLOAT,
    hostname VARCHAR(100)
);
