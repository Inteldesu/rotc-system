-- Create the Database
CREATE DATABASE IF NOT EXISTS rotc_db;
USE rotc_db;

-- Create Users Table (Handles Login/Registration)
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    role VARCHAR(20) DEFAULT 'cadet',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create Attendance Table (Handles Monitoring)
CREATE TABLE IF NOT EXISTS attendance (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50), -- Links to the person who submitted
    name VARCHAR(100) NOT NULL,
    rank VARCHAR(50),
    date VARCHAR(50),
    FOREIGN KEY (username) REFERENCES users(username) ON DELETE CASCADE
);

-- Insert the System Owner (Admin) 
-- Note: Python's werkzeug generate_password_hash is recommended for the password
-- But for a manual insert, ensure you use the admin123 / 12345678 credentials via app.py
INSERT IGNORE INTO users (username, password, role) 
VALUES ('admin123', 'pbkdf2:sha256:260000$ManualHashGoesHere', 'admin');