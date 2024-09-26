from flask import Flask, render_template, request, redirect, url_for, session, flash
from cryptography.fernet import Fernet
import os
import json

app = Flask(__name__)

# Секретный ключ для сессий
app.secret_key = ''

# Путь к файлу для хранения паролей
PASSWORDS_FILE = 'passwords.json'

# Генерация или загрузка ключа для шифрования
if os.path.exists('key.key'):
    with open('key.key', 'rb') as key_file:
        key = key_file.read()
else:
    key = Fernet.generate_key()
    with open('key.key', 'wb') as key_file:
        key_file.write(key)

cipher = Fernet(key)

# Загрузка паролей из файла
def load_passwords():
    if os.path.exists(PASSWORDS_FILE):
        with open(PASSWORDS_FILE, 'r') as f:
            return json.load(f)
    return {}

# Сохранение паролей в файл
def save_passwords(passwords):
    with open(PASSWORDS_FILE, 'w') as f:
        json.dump(passwords, f)

@app.route('/')
def index():
    if 'logged_in' in session and session['logged_in']:
        passwords = load_passwords()
        decrypted_passwords = {k: cipher.decrypt(v.encode()).decode() for k, v in passwords.items()}
        return render_template('index.html', passwords=decrypted_passwords, username=session.get('username'))
    else:
        return redirect(url_for('login'))

# Маршрут для страницы авторизации
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        # Простая проверка логина и пароля
        if username == 'admin' and password == '':  # Замените на свой логин/пароль
            session['logged_in'] = True
            session['username'] = username  # Сохраняем логин в сессии для отображения на странице
            return redirect(url_for('index'))  # Перенаправление на главную страницу после успешной авторизации
        else:
            flash('Неверные имя пользователя или пароль')  # Сообщение об ошибке

    return render_template('login.html')  # Показ формы входа

@app.route('/logout')
def logout():
    session.pop('logged_in', None)  # Удалить статус авторизации
    session.pop('username', None)  # Удалить имя пользователя из сессии
    return redirect(url_for('login'))

@app.route('/add', methods=['POST'])
def add_password():
    if 'logged_in' in session and session['logged_in']:
        service = request.form['service']
        password = request.form['password']

        encrypted_password = cipher.encrypt(password.encode()).decode()

        passwords = load_passwords()
        passwords[service] = encrypted_password
        save_passwords(passwords)

        return redirect(url_for('index'))
    else:
        return redirect(url_for('login'))

@app.route('/delete/<service>', methods=['POST'])
def delete_password(service):
    if 'logged_in' in session and session['logged_in']:
        passwords = load_passwords()
        if service in passwords:
            del passwords[service]
            save_passwords(passwords)

        return redirect(url_for('index'))
    else:
        return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)

    app.run(debug=True)
