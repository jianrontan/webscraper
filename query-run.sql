CREATE DATABASE carousell;
CREATE TABLE carousell.products (
    id INT AUTO_INCREMENT,
    name VARCHAR(255),
    price DECIMAL(10, 2),
    link VARCHAR(1024),
    date_time DATETIME,
    PRIMARY KEY(id)
);