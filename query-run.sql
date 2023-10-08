CREATE DATABASE carousell;
CREATE TABLE carousell.products (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255),
    price DECIMAL(10, 2),
    date_time DATETIME
);