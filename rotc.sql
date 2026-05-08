CREATE DATABASE IF NOT EXISTS rotc_db;
USE rotc_db;

-- Users Table (Plain text passwords)
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    role VARCHAR(20) DEFAULT 'cadet'
);

-- Attendance Table
USE rotc_db;

-- Drop the old table so we can create it with the correct columns
USE rotc_db;

-- Drop existing tables to ensure a clean start
DROP TABLE IF EXISTS equipment;
DROP TABLE IF EXISTS attendance;

-- Create Attendance Table
CREATE TABLE attendance (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    rank VARCHAR(50),
    platoon VARCHAR(50),
    status VARCHAR(50),
    date_recorded VARCHAR(50),
    submitted_by VARCHAR(50),
    FOREIGN KEY (submitted_by) REFERENCES users(username)
);

-- Create Equipment Table
CREATE TABLE equipment (
    id INT AUTO_INCREMENT PRIMARY KEY,
    borrower VARCHAR(100) NOT NULL, -- This is the column your error was missing
    item VARCHAR(100),
    quantity INT,
    borrow_date VARCHAR(50),
    submitted_by VARCHAR(50),
    FOREIGN KEY (submitted_by) REFERENCES users(username)
);
-- Insert the System Owner (Admin) 
-- Note: Python's werkzeug generate_password_hash is recommended for the password
-- But for a manual insert, ensure you use the admin123 / 12345678 credentials via app.py
INSERT IGNORE INTO users (username, password, role) 
VALUES ('admin', 'koishi', 'admin');