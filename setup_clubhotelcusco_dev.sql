-- prepares a MySQL server for the project

CREATE DATABASE IF NOT EXISTS clubhotelcusco_db;
CREATE USER IF NOT EXISTS 'clubhotelcusco'@'localhost' IDENTIFIED BY '951chcpwd753';
GRANT ALL PRIVILEGES ON `clubhotelcusco_db`.* TO 'clubhotelcusco'@'localhost';
GRANT SELECT ON `performance_schema`.* TO 'clubhotelcusco'@'localhost';
FLUSH PRIVILEGES;
