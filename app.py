from flask import Flask, request, jsonify, redirect, url_for, session, render_template_string
import secrets
import time
import json
import os

app = Flask(__name__)
app.secret_key = 'sua_chave_secreta'  # Defina uma chave secreta para sessões

# Armazenamento de dados de usuários
users_file = 'users.json'

# Carrega os usuários do arquivo JSON
def load_users():
    if os.path.exists(users_file):
        with open(users_file, 'r') as f:
            return json.load(f)
    return {}

# Salva os usuários no arquivo JSON
def save_users(users):
    with open(users_file, 'w') as f:
        json.dump(users, f)

# Dados de exemplo
allowed_users = load_users()
admin_username = "admin"
admin_password = "admin123"

# Função para gerar uma chave aleatória
def generate_key():
    return secrets.token_hex(16)  # Gera uma chave hexadecimal de 16 bytes

# Função para verificar se a chave ainda é válida
def is_key_valid(username):
    if username in allowed_users:
        user_data = allowed_users[username]
        current_time = time.time()
        # Verifica se o usuário ainda tem acessos disponíveis
        if user_data['visits'] < user_data['max_visits']:
            return True
    return False

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        username = request.form.get('username')
        if username in allowed_users and is_key_valid(username):
            # Aumenta o contador de acessos
            allowed_users[username]['visits'] += 1
            save_users(allowed_users)  # Salva as alterações no arquivo JSON
            key = generate_key()
            return f'''
            <!DOCTYPE html>
            <html lang="en">
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>Access Key</title>
            </head>
            <body>
                <h1>Access Key</h1>
                <p>{key}</p>
            </body>
            </html>
            '''
        return "Acesso negado!"
    
    return '''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Login</title>
    </head>
    <body>
        <h1>Login</h1>
        <form method="post">
            <label for="username">Usuário:</label>
            <input type="text" id="username" name="username" required>
            <button type="submit">Obter Chave</button>
        </form>
        <p>Entre em contato para ter acesso: <a href="https://t.me/Keno_venas">Keno Venas</a></p>
    </body>
    </html>
    '''

@app.route('/admin', methods=['GET', 'POST'])
def admin_panel():
    if 'admin_logged_in' not in session:
        return redirect(url_for('admin_login_page'))

    if request.method == 'POST':
        username = request.form.get('username')
        max_visits = int(request.form.get('max_visits'))
        # Atualiza ou adiciona o usuário
        allowed_users[username] = {"visits": 0, "max_visits": max_visits}
        save_users(allowed_users)  # Salva as alterações no arquivo JSON
        return redirect(url_for('admin_panel'))

    return render_template_string('''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>Painel de Administração</title>
    </head>
    <body>
        <h1>Painel de Administração</h1>
        <h2>Usuários</h2>
        <ul>
        {% for user, data in users.items() %}
            <li>{{ user }} - Acessos: {{ data.visits }} / Máximo: {{ data.max_visits }}</li>
        {% endfor %}
        </ul>
        <h2>Adicionar ou Editar Usuário</h2>
        <form method="post">
            <label for="username">Usuário:</label>
            <input type="text" id="username" name="username" required>
            <label for="max_visits">Máximo de Acessos:</label>
            <input type="number" id="max_visits" name="max_visits" required>
            <button type="submit">Salvar</button>
        </form>
        <a href="/logout">Logout</a>
    </body>
    </html>
    ''', users=allowed_users)

@app.route('/admin_login', methods=['GET', 'POST'])
def admin_login_page():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if username == admin_username and password == admin_password:
            session['admin_logged_in'] = True
            return redirect(url_for('admin_panel'))
        return "Login falhou!"
    
    return '''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>Login Administrador</title>
    </head>
    <body>
        <h1>Login Administrador</h1>
        <form method="post">
            <label for="username">Usuário:</label>
            <input type="text" id="username" name="username" required>
            <label for="password">Senha:</label>
            <input type="password" id="password" name="password" required>
            <button type="submit">Login</button>
        </form>
    </body>
    </html>
    '''

@app.route('/logout')
def logout():
    session.pop('admin_logged_in', None)
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)
