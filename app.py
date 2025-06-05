from flask import Flask, request, jsonify, render_template
from datetime import datetime
import random
import string
import sqlite3

app = Flask(__name__)

DB_FILE = 'passwords.db'

def init_db():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            length INTEGER,
            include_numbers BOOLEAN,
            include_specials BOOLEAN,
            count INTEGER,
            passwords TEXT
        )
    ''')
    conn.commit()
    conn.close()

init_db()

def generate_password(length, use_numbers, use_specials):
    chars = string.ascii_letters
    if use_numbers:
        chars += string.digits
    if use_specials:
        chars += string.punctuation
    return ''.join(random.choice(chars) for _ in range(length))

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/history.html')
def history_page():
    return render_template('history.html')

@app.route('/generate-password', methods=['POST'])
def generate_password_api():
    data = request.json
    length = int(data.get('length', 12))
    include_numbers = bool(data.get('include_numbers', False))
    include_specials = bool(data.get('include_specials', False))
    count = int(data.get('count', 1))

    passwords = [generate_password(length, include_numbers, include_specials) for _ in range(count)]

    # Save to DB
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('''
        INSERT INTO history (timestamp, length, include_numbers, include_specials, count, passwords)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (datetime.now().isoformat(), length, include_numbers, include_specials, count, '\n'.join(passwords)))
    conn.commit()
    conn.close()

    return jsonify({'passwords': passwords})

@app.route('/history', methods=['GET'])
def get_history():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('SELECT timestamp, length, include_numbers, include_specials, count, passwords FROM history ORDER BY id DESC')
    rows = c.fetchall()
    conn.close()

    history = [
        {
            'timestamp': row[0],
            'length': row[1],
            'include_numbers': bool(row[2]),
            'include_specials': bool(row[3]),
            'count': row[4],
            'passwords': row[5].split('\n')
        }
        for row in rows
    ]

    return jsonify({'history': history})

if __name__ == '__main__':
    app.run(debug=True)
