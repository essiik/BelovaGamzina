from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3
import hashlib
import re

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'

def init_db():
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            email TEXT NOT NULL UNIQUE,
            password_hash TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def validate_email(email):
    pattern = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    return re.match(pattern, email) is not None

@app.route('/')
def register_form():
    return render_template('register.html')

@app.route('/main')
def main_page():
    return render_template('main.html')

@app.route('/register', methods=['POST'])
def register():
    username = request.form.get('username', '').strip()
    email = request.form.get('email', '').strip()
    password = request.form.get('password', '').strip()

    if not username or not email or not password:
        flash('Заполните все поля!', 'error')
        return redirect(url_for('register_form'))
    if len(username) < 3:
        flash('Имя пользователя должно содержать минимум 3 символа', 'error')
        return redirect(url_for('register_form'))
    if not validate_email(email):
        flash('Введите корректный адрес электронной почты', 'error')
        return redirect(url_for('register_form'))
    if len(password) < 6:
        flash('Пароль должен содержать не менее 6 символов', 'error')
        return redirect(url_for('register_form'))

    password_hash = hash_password(password)

    try:
        conn = sqlite3.connect('users.db')
        cursor = conn.cursor()
        cursor.execute(
            'INSERT INTO users (username, email, password_hash) VALUES (?, ?, ?)',
            (username, email, password_hash)
        )
        conn.commit()
        conn.close()
        flash(f'Аккаунт для пользователя "{username}" успешно создан!', 'success')
        return redirect(url_for('main_page'))
    except sqlite3.IntegrityError as e:
        if 'username' in str(e):
            flash('Имя пользователя уже занято!', 'error')
        else:
            flash('Пользователь с таким email уже существует!', 'error')
        return redirect(url_for('register_form'))

if __name__ == '__main__':
    init_db()
    app.run(debug=True, port=5001)
