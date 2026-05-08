# app.py
from flask import Flask, render_template, request, jsonify, session, redirect
import pymysql
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'rotc_direct_mysql_key'

# MYSQL CONFIGURATION
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '',
    'database': 'rotc_db',
    'cursorclass': pymysql.cursors.DictCursor
}

def get_db():
    return pymysql.connect(**db_config)

# INITIALIZE DATABASE AND TABLES
def init_db():
    conn = get_db()
    with conn.cursor() as cursor:
        # Create Users Table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INT AUTO_INCREMENT PRIMARY KEY,
                username VARCHAR(50) UNIQUE NOT NULL,
                password VARCHAR(255) NOT NULL,
                role VARCHAR(20) DEFAULT 'cadet'
            )
        """)
        # Create Attendance Table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS attendance (
                id INT AUTO_INCREMENT PRIMARY KEY,
                username VARCHAR(50),
                name VARCHAR(100),
                rank VARCHAR(50),
                date VARCHAR(50)
            )
        """)
        # Create Owner (admin123 / 12345678)
        cursor.execute("SELECT * FROM users WHERE username = 'admin123'")
        if not cursor.fetchone():
            hashed_pw = generate_password_hash('12345678')
            cursor.execute("INSERT INTO users (username, password, role) VALUES (%s, %s, %s)", 
                           ('admin123', hashed_pw, 'admin'))
    conn.commit()
    conn.close()

# AUTH ROUTES
@app.route('/login', methods=['POST'])
def login():
    data = request.json
    conn = get_db()
    with conn.cursor() as cursor:
        cursor.execute("SELECT * FROM users WHERE username = %s", (data['username'],))
        user = cursor.fetchone()
    conn.close()

    if user and check_password_hash(user['password'], data['password']):
        session['user'] = user['username']
        session['role'] = user['role']
        return jsonify({"success": True})
    return jsonify({"success": False}), 401

@app.route('/register', methods=['POST'])
def register():
    data = request.json
    conn = get_db()
    try:
        with conn.cursor() as cursor:
            hashed = generate_password_hash(data['password'])
            cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (data['username'], hashed))
        conn.commit()
        return jsonify({"success": True})
    except:
        return jsonify({"success": False, "message": "User exists"}), 400
    finally:
        conn.close()

# DATA ROUTES
@app.route('/')
def home():
    logged_in = 'user' in session
    role = session.get('role', 'cadet')
    records = []
    if logged_in:
        conn = get_db()
        with conn.cursor() as cursor:
            if role == 'admin':
                cursor.execute("SELECT * FROM attendance")
            else:
                cursor.execute("SELECT * FROM attendance WHERE username = %s", (session['user'],))
            records = cursor.fetchall()
        conn.close()
    return render_template('index.html', logged_in=logged_in, role=role, records=records)

@app.route('/add', methods=['POST'])
def add():
    if 'user' not in session: return jsonify({"error": "No Auth"}), 401
    data = request.json
    conn = get_db()
    with conn.cursor() as cursor:
        cursor.execute("INSERT INTO attendance (username, name, rank, date) VALUES (%s, %s, %s, %s)", 
                       (session['user'], data['name'], data['rank'], data['date']))
    conn.commit()
    conn.close()
    return jsonify({"success": True})

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

if __name__ == "__main__":
    init_db()
    app.run(debug=True)