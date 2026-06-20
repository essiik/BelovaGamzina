# ==================================================================
# ИНТЕРНЕТ-МАГАЗИН "LACY INTIMACY" — СЕРВЕРНАЯ ЧАСТЬ (FLASK)
# ==================================================================

# Импорт необходимых библиотек
from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3      # Для работы с базой данных SQLite
import hashlib      # Для хеширования паролей
import re           # Для проверки email через регулярное выражение

# ------------------------------------------------------------------
# НАСТРОЙКА ПРИЛОЖЕНИЯ
# ------------------------------------------------------------------
app = Flask(__name__)
app.secret_key = 'your_secret_key_here'   # Нужен для flash-сообщений

# ==================================================================
# 1. РАБОТА С БАЗОЙ ДАННЫХ (SQLite)
# ==================================================================

def init_db():
    """
    Инициализация базы данных.
    Создаёт файл users.db и таблицу users, если они ещё не существуют.
    Таблица содержит поля:
        - id: уникальный идентификатор (автоинкремент)
        - username: имя пользователя (уникальное)
        - email: электронная почта (уникальная)
        - password_hash: хеш пароля (SHA256)
    """
    conn = sqlite3.connect('users.db')          # Подключаемся к БД (файл создаётся автоматически)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            email TEXT NOT NULL UNIQUE,
            password_hash TEXT NOT NULL
        )
    ''')
    conn.commit()      # Сохраняем изменения
    conn.close()       # Закрываем соединение

def hash_password(password):
    """Хеширует пароль с помощью алгоритма SHA256."""
    return hashlib.sha256(password.encode()).hexdigest()

def validate_email(email):
    """
    Проверяет корректность email с помощью регулярного выражения.
    Возвращает True, если email соответствует стандартному формату.
    """
    pattern = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    return re.match(pattern, email) is not None

# ==================================================================
# 2. МАРШРУТЫ (ROUTES) — СТРАНИЦЫ И ОБРАБОТЧИКИ
# ==================================================================

@app.route('/')
def register_form():
    """
    Отображает страницу регистрации (register.html).
    Пользователь видит форму для ввода имени, email и пароля.
    """
    return render_template('register.html')

@app.route('/main')
def main_page():
    """
    Отображает главную страницу интернет-магазина (main.html).
    После успешной регистрации пользователь перенаправляется сюда.
    """
    return render_template('main.html')

@app.route('/register', methods=['POST'])
def register():
    """
    Обрабатывает данные, отправленные из формы регистрации.
    Выполняет валидацию, хеширует пароль и сохраняет нового пользователя в БД.
    """
    # Получаем данные из формы
    username = request.form.get('username', '').strip()
    email = request.form.get('email', '').strip()
    password = request.form.get('password', '').strip()

    # ---------- ВАЛИДАЦИЯ ПОЛЕЙ ----------
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

    # Хешируем пароль перед сохранением
    password_hash = hash_password(password)

    # ---------- СОХРАНЕНИЕ В БАЗУ ДАННЫХ ----------
    try:
        conn = sqlite3.connect('users.db')          # Открываем соединение
        cursor = conn.cursor()
        cursor.execute(
            'INSERT INTO users (username, email, password_hash) VALUES (?, ?, ?)',
            (username, email, password_hash)
        )
        conn.commit()                               # Фиксируем вставку
        conn.close()                                # Закрываем соединение

        flash(f'Аккаунт для пользователя "{username}" успешно создан!', 'success')
        return redirect(url_for('main_page'))       # Редирект на главную страницу

    except sqlite3.IntegrityError as e:
        # Обрабатываем ошибку уникальности (пользователь с таким именем или email уже существует)
        if 'username' in str(e):
            flash('Имя пользователя уже занято!', 'error')
        else:
            flash('Пользователь с таким email уже существует!', 'error')
        return redirect(url_for('register_form'))

# ==================================================================
# 3. ЗАПУСК ПРИЛОЖЕНИЯ
# ==================================================================
if __name__ == '__main__':
<<<<<<< Updated upstream
    init_db()                         # Создаём таблицу при старте
    app.run(debug=True, port=5001)    # Запускаем сервер на порту 5001
=======
    init_db()
    app.run(debug=True, port=5001)
>>>>>>> Stashed changes
