-- prepares a MySQL server for the project

CREATE DATABASE IF NOT EXISTS clubhotelcusco_test_db;
CREATE USER IF NOT EXISTS 'clubhotelcuscot'@'localhost' IDENTIFIED BY '951chctpwd753';
GRANT ALL PRIVILEGES ON `clubhotelcusco_test_db`.* TO 'clubhotelcuscot'@'localhost';
GRANT SELECT ON `performance_schema`.* TO 'clubhotelcuscot'@'localhost';
FLUSH PRIVILEGES;
