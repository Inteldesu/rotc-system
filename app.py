from flask import Flask, request, session, redirect, render_template
import pymysql
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import date

app = Flask(__name__)
app.secret_key = 'rotc_direct_mysql_key'

# DB CONFIG
db_config = {
    'host': 'localhost',
    'user': 'ali',
    'password': 'toshinoukyouko',
    'database': 'rotc_db',
    'cursorclass': pymysql.cursors.DictCursor
}

def get_db():
    return pymysql.connect(**db_config)

# INIT DB
# Matches your SQL schema (users + attendance with FK)
def init_db():
    conn = get_db()
    with conn.cursor() as cursor:

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INT AUTO_INCREMENT PRIMARY KEY,
                username VARCHAR(50) UNIQUE NOT NULL,
                password VARCHAR(255) NOT NULL,
                role VARCHAR(20) DEFAULT 'cadet',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS attendance (
                id INT AUTO_INCREMENT PRIMARY KEY,
                username VARCHAR(50),
                name VARCHAR(100) NOT NULL,
                rank VARCHAR(50),
                date VARCHAR(50),
                FOREIGN KEY (username) REFERENCES users(username) ON DELETE CASCADE
            )
        """)

        # Ensure admin exists (matches your SQL: admin / koishi)
        cursor.execute("SELECT * FROM users WHERE username=%s", ('admin',))
        if not cursor.fetchone():
            cursor.execute(
                "INSERT INTO users (username, password, role) VALUES (%s, %s, %s)",
                ('admin', generate_password_hash('koishi'), 'admin')
            )

    conn.commit()
    conn.close()

# ---------------- HOME ----------------
@app.route('/')
def home():
    if 'user' not in session:
        return redirect('/login')

    conn = get_db()
    with conn.cursor() as cursor:
        if session.get('role') == 'admin':
            cursor.execute("SELECT * FROM attendance")
        else:
            cursor.execute("SELECT * FROM attendance WHERE username=%s", (session['user'],))
        records = cursor.fetchall()
    conn.close()

    return render_template(
        'index.html',
        user=session['user'],
        role=session['role'],
        records=records
    )

# ---------------- LOGIN ----------------
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')

    username = request.form.get('username')
    password = request.form.get('password')

    conn = get_db()
    with conn.cursor() as cursor:
        cursor.execute("SELECT * FROM users WHERE username=%s", (username,))
        user = cursor.fetchone()
    conn.close()

    if user and user['password'] == password:
        session['user'] = user['username']
        session['role'] = user['role']
        return redirect('/')

    return "LOGIN FAILED"

# ---------------- REGISTER ----------------
@app.route('/register', methods=['POST'])
def register():
    username = request.form.get('username')
    password = request.form.get('password')

    conn = get_db()
    try:
        with conn.cursor() as cursor:
            cursor.execute(
                "INSERT INTO users (username, password) VALUES (%s, %s)",
                (username, generate_password_hash(password))
            )
        conn.commit()
        return redirect('/login')
    except:
        return "USER EXISTS"
    finally:
        conn.close()

# ---------------- ADD ATTENDANCE ----------------
@app.route('/add', methods=['POST'])
def add():
    if 'user' not in session:
        return redirect('/login')

    name = request.form.get('name')
    rank = request.form.get('rank')

    conn = get_db()
    with conn.cursor() as cursor:
        cursor.execute("""
            INSERT INTO attendance (username, name, rank, date)
            VALUES (%s, %s, %s, %s)
        """, (session['user'], name, rank, str(date.today())))

    conn.commit()
    conn.close()

    return redirect('/')

# ---------------- LOGOUT ----------------
@app.route('/logout')
def logout():
    session.clear()
    return redirect('/login')

if __name__ == '__main__':
    init_db()
    app.run(debug=True, port=5001)