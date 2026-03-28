from flask import Flask, render_template, request
import sqlite3
import hashlib
from datetime import datetime

app = Flask(__name__)

# Database table banana
def init_db():
    conn = sqlite3.connect('cyber_logs.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS incidents 
                 (id INTEGER PRIMARY KEY, user TEXT, type TEXT, msg TEXT, token TEXT, time TEXT)''')
    conn.commit()
    conn.close()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/report', methods=['POST'])
def report():
    u_name = request.form['u_name']
    u_type = request.form['u_type']
    u_msg = request.form['u_msg']
    time_stamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # SECURITY FEATURE: SHA-256 Hashing (Cyber Security Concept)
    secure_token = hashlib.sha256(f"{u_name}{time_stamp}".encode()).hexdigest()

    conn = sqlite3.connect('cyber_logs.db')
    c = conn.cursor()
    c.execute("INSERT INTO incidents (user, type, msg, token, time) VALUES (?, ?, ?, ?, ?)",
              (u_name, u_type, u_msg, secure_token, time_stamp))
    conn.commit()
    conn.close()
    return f"<h3>Success! Secure Token Generated: {secure_token}</h3><a href='/'>Back</a>"

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
