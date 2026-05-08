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

CREATE TABLE IF NOT EXISTS team_members (
    id INT AUTO_INCREMENT PRIMARY KEY,
    full_name VARCHAR(100) NOT NULL,
    username VARCHAR(50),
    role VARCHAR(100),
    about_me TEXT,
    profile_image_path VARCHAR(255),
    github_link VARCHAR(255),
    facebook_link VARCHAR(255),
    accent_color VARCHAR(7) DEFAULT '#10b981' -- Emerald green default
);

TRUNCATE TABLE team_members;

INSERT INTO team_members 
(full_name, username, role, about_me, profile_image_path, github_link, facebook_link, accent_color)
VALUES 
(
    'Cyrus Troy Bazar', 
    'Alieelinux', 
    'Backend, Frontend, almost Everything', 
    'An Ilocano student living in the holy lands of Isabela, currently attending at Isabela State University. Specialized in Backend development and System Architecture.', 
    'https://media1.tenor.com/m/n6zppmoEdZUAAAAC/koishi-koishi-happy-love.gif', 
    'https://github.com/Alieelinux', 
    'https://www.facebook.com/KoishiKomeiji0', 
    '#ff00ea' -- Pink
),
(
"Lovelee Flomarjoy T. Madamba",
"asdfghjkl_lvlee",
"ganda lang",
"it's for me to know and it's for you to find out",
"/static/Madamba.jpg",
NULL,
"https://www.facebook.com/share/18QDHB69Wc/",
'#ff00ea'
),
(
"Nelo M. Cabab",
"Nelshima",
"core user",
"Mabait",
"/static/nelo.jpg",
NULL,
"https://www.facebook.com/share/1EFi9LAXbV/",
"#FFC0CB"
),
(
    'Adrian Intel Pil V. De Vera', 
    'Intedesu', 
    'Role model', 
    'mas mabait.', 
    '/static/intel.jpg', 
    NULL, 
    'https://www.facebook.com/AdrianIntelDeVera25', 
    '#7F00FF'
),
(
    'Mark Jhon Paul L. Pace', 
    'idgaf_pcee', 
    'Pabohat', 
    "it's all about me.", 
    '/static/pace.jpg', 
    NULL, 
    'https://www.facebook.com/mrkyohan/', 
    '#BA8E23'
)