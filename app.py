from flask import Flask, render_template, request, redirect, session, url_for
import pymysql
from dotenv import load_dotenv
import os

load_dotenv()

db_server = os.getenv("DB_SERVER", "localhost")
db_user = os.getenv("DB_USER", 'root')
db_password = os.getenv("DB_PASSWORD", "")
db_databasename = os.getenv("DB_DATABASE", "athlete_dashboard")
db_port = int(os.getenv("DB_PORT", 6969))

app = Flask(__name__)
app.secret_key = 'rotc_direct_mysql_key'

# Database Configuration
db_config = {
    'host': db_server,
    'user': db_user,
    'password': db_password,
    'database': db_databasename,
    'cursorclass': pymysql.cursors.DictCursor
}

def get_db():
    return pymysql.connect(**db_config)

@app.route('/')
@app.route('/')
def index():
    if 'user' not in session:
        return redirect(url_for('login'))
    
    conn = get_db()
    with conn.cursor() as cursor:
        # Fetch data for tables
        cursor.execute("SELECT * FROM attendance")
        att_records = cursor.fetchall()
        
        cursor.execute("SELECT * FROM equipment")
        eq_records = cursor.fetchall()

        # --- NEW: CALCULATE TOTALS ---
        # Count attendance rows
        total_attendance = len(att_records)
        
        # Sum the 'quantity' column for equipment
        cursor.execute("SELECT SUM(quantity) AS total_qty FROM equipment")
        result = cursor.fetchone()
        total_equipment = result['total_qty'] if result['total_qty'] else 0

    conn.close()
    
    return render_template('index.html', 
                           attendance=att_records, 
                           equipment=eq_records,
                           total_att=total_attendance,
                           total_eq=total_equipment,
                           user=session['user'])

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        conn = get_db()
        with conn.cursor() as cursor:
            # Plain text comparison
            cursor.execute("SELECT * FROM users WHERE username=%s AND password=%s", (username, password))
            user = cursor.fetchone()
        conn.close()

        if user:
            session['user'] = user['username']
            return redirect(url_for('index'))
        return "Invalid Username or Password"
    return render_template('login.html')

@app.route('/register', methods=['POST'])
def register():
    username = request.form['username']
    password = request.form['password'] # Stored as plain text
    
    conn = get_db()
    try:
        with conn.cursor() as cursor:
            cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, password))
        conn.commit()
    except:
        return "User registration failed (User might already exist)"
    finally:
        conn.close()
    return redirect(url_for('login'))

@app.route('/add_attendance', methods=['POST'])
def add_attendance():
    if 'user' not in session: return redirect(url_for('login'))
    
    conn = get_db()
    with conn.cursor() as cursor:
        cursor.execute("""
            INSERT INTO attendance (name, rank, platoon, status, date_recorded, submitted_by)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (request.form['cadetName'], request.form['rank'], request.form['platoon'], 
              request.form['status'], request.form['attendanceDate'], session['user']))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

@app.route('/add_equipment', methods=['POST'])
def add_equipment():
    if 'user' not in session:
        return redirect(url_for('login'))
    
    # Get values from the HTML form 'name' attributes
    borrower_val = request.form.get('borrowerName')
    equipment_item = request.form.get('equipment')
    qty = request.form.get('quantity')
    b_date = request.form.get('borrowDate')

    conn = get_db()
    try:
        with conn.cursor() as cursor:
            # The words inside (borrower, item, quantity...) MUST match the SQL columns
            cursor.execute("""
                INSERT INTO equipment (borrower, item, quantity, borrow_date, submitted_by)
                VALUES (%s, %s, %s, %s, %s)
            """, (borrower_val, equipment_item, qty, b_date, session['user']))
        conn.commit()
    finally:
        conn.close()

    return redirect(url_for('index'))

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True, port=db_port)