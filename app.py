from flask import Flask, render_template, request, jsonify, session, redirect
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import os

app = Flask(__name__)
app.secret_key = 'rotc_tactical_key_2024'

# DATABASE CONFIG
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///rotc_system.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# MODELS
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    role = db.Column(db.String(20), default='cadet')

class Attendance(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50))
    name = db.Column(db.String(100))
    rank = db.Column(db.String(50))
    status = db.Column(db.String(50))
    date = db.Column(db.String(50))

# AUTH ROUTES
@app.route('/login', methods=['POST'])
def login():
    data = request.json
    user = User.query.filter_by(username=data['username']).first()
    if user and check_password_hash(user.password, data['password']):
        session['user'] = user.username
        session['role'] = user.role
        return jsonify({"success": True})
    return jsonify({"success": False}), 401

@app.route('/register', methods=['POST'])
def register():
    data = request.json
    if User.query.filter_by(username=data['username']).first():
        return jsonify({"success": False, "message": "User exists"}), 400
    hashed = generate_password_hash(data['password'])
    new_user = User(username=data['username'], password=hashed)
    db.session.add(new_user)
    db.session.commit()
    return jsonify({"success": True})

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

@app.route('/')
def home():
    logged_in = 'user' in session
    role = session.get('role', 'cadet')
    records = []
    if logged_in:
        records = Attendance.query.all() if role == 'admin' else Attendance.query.filter_by(username=session['user']).all()
    return render_template('index.html', logged_in=logged_in, role=role, records=records)

@app.route('/add', methods=['POST'])
def add():
    if 'user' not in session: return jsonify({"error": "No Auth"}), 401
    data = request.json
    db.session.add(Attendance(username=session['user'], name=data['name'], rank=data['rank'], status='Present', date=data['date']))
    db.session.commit()
    return jsonify({"success": True})

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        if not User.query.filter_by(username='admin123').first():
            db.session.add(User(username='admin123', password=generate_password_hash('12345678'), role='admin'))
            db.session.commit()
    app.run(debug=True)