# CREATE DATABASE stock_notifications;

USE stock_notifications;

CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(255) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL
);

CREATE TABLE UserStock (
    id INT AUTO_INCREMENT PRIMARY KEY,          -- Unique identifier for each entry
    user_id INT NOT NULL,                       -- Foreign key linking to the User table
    stock_symbol VARCHAR(10) NOT NULL,          -- Stock symbol, e.g., "AAPL"
    threshold DECIMAL(10, 2) NOT NULL,          -- User-defined threshold price
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP, -- Timestamp of when the stock was added
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP, -- Timestamp of last update
    FOREIGN KEY (user_id) REFERENCES users(id)  -- Assuming 'Users' table has 'id' as primary key
);

alter table users drop column firebase_token;
