from flask import Flask, request, jsonify, render_template_string, redirect, url_for, session
import secrets
import time
from functools import wraps

app = Flask(__name__)
app.secret_key = 'sua_chave_secreta_aqui'  # Defina uma chave secreta para sessões

# Armazenamento para chave, timestamp e usuários permitidos
key_data = {
    "key": None,
    "timestamp": None
}

# Usuários permitidos e contagem de acessos
allowed_users = {
    "usuario1": {"visits": 0, "max_visits": 5},
    "usuario2": {"visits": 0, "max_visits": 3},
    "usuario_configurado": {"visits": 0, "max_visits": 10}
}

# Dados do administrador
admin_username = "admin"  # Nome de usuário do administrador
admin_password = "senha"  # Senha do administrador

# Decorador para proteger rotas administrativas
def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'username' not in session:
            return redirect(url_for('admin_login'))
        return f(*args, **kwargs)
    return decorated_function

# Função para gerar uma chave aleatória
def generate_key():
    return secrets.token_hex(16)

# Função para verificar se a chave ainda é válida
def is_key_valid():
    if key_data["key"] and key_data["timestamp"]:
        current_time = time.time()
        if current_time - key_data["timestamp"] <= 300:
            return True
    return False

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        username = request.form.get('username')
        if username in allowed_users:
            user_data = allowed_users[username]
            
            if user_data["visits"] >= user_data["max_visits"]:
                return render_template_string(f'''
                    <!DOCTYPE html>
                    <html lang="en">
                    <head>
                        <meta charset="UTF-8">
                        <meta name="viewport" content="width=device-width, initial-scale=1.0">
                        <title>Acesso Negado</title>
                    </head>
                    <body>
                        <h1>Acesso Negado</h1>
                        <p>Você atingiu o limite máximo de acessos.</p>
                    </body>
                    </html>
                ''')

            user_data["visits"] += 1
            remaining_accesses = user_data["max_visits"] - user_data["visits"]
            
            if not is_key_valid():
                key_data["key"] = generate_key()
                key_data["timestamp"] = time.time()
                
            return render_template_string(f'''
            <!DOCTYPE html>
            <html lang="en">
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>Access Key</title>
                <style>
                    body {{
                        display: flex;
                        justify-content: center;
                        align-items: center;
                        height: 100vh;
                        margin: 0;
                        position: relative;
                        flex-direction: column;
                    }}
                    .content {{
                        text-align: center;
                        margin-top: 20px;
                    }}
                    .author {{
                        position: absolute;
                        top: 10px;
                        left: 10px;
                        color: #000;
                        font-size: 18px;
                    }}
                    .banner-telegram {{
                        position: absolute;
                        top: 10px;
                        right: 10px;
                        background-color: #0088cc;
                        padding: 10px;
                        border-radius: 5px;
                        box-shadow: 0 2px 4px rgba(0,0,0,0.2);
                    }}
                    .banner-telegram a {{
                        color: #ffcc00;
                        text-decoration: none;
                        font-weight: bold;
                    }}
                    .admin-panel {{
                        position: fixed;
                        bottom: 10px;
                        left: 10px;
                        background-color: #f0f0f0;
                        padding: 10px;
                        border: 1px solid #ccc;
                        border-radius: 5px;
                        box-shadow: 0 2px 4px rgba(0,0,0,0.2);
                    }}
                </style>
            </head>
            <body>
                <div class="author">Autor = Keno Venas</div>
                <div class="banner-telegram">
                    <a href="https://t.me/Keno_venas" target="_blank">Grupo do Telegram</a>
                </div>
                <div class="content">
                    <h1>Access Key</h1>
                    <p>Chave: {key_data["key"]}</p>
                    <p>Você já acessou {user_data["visits"]} de {user_data["max_visits"]} vezes.</p>
                    <p>Restam {remaining_accesses} acessos.</p>
                </div>
                <div class="admin-panel">
                    <h3>Painel Admin</h3>
                    <form action="/admin_login" method="post">
                        <input type="text" name="username" placeholder="Usuário" required>
                        <input type="password" name="password" placeholder="Senha" required>
                        <button type="submit">Login Admin</button>
                    </form>
                </div>
            </body>
            </html>
            ''')

        else:
            return "Acesso negado"

    return '''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Login</title>
        <style>
            .telegram-button {{
                background-color: #0088cc;
                color: white;
                padding: 10px 20px;
                border: none;
                border-radius: 5px;
                text-align: center;
                text-decoration: none;
                display: inline-block;
                font-size: 16px;
                margin-top: 20px;
                cursor: pointer;
            }}
            .telegram-button:hover {{
                background-color: #005f99;
            }}
        </style>
    </head>
    <body>
        <h1>Digite seu usuário</h1>
        <form method="POST">
            <input type="text" name="username" required>
            <button type="submit">Acessar</button>
        </form>
        <p>Entrar em contato para ter acesso:</p>
        <a href="https://t.me/Keno_venas" target="_blank" class="telegram-button">Keno Venas</a>
    </body>
    </html>
    '''

@app.route('/admin', methods=['GET'])
@admin_required
def admin_panel():
    return render_template_string('''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Painel Administrativo</title>
    </head>
    <body>
        <h1>Painel Administrativo</h1>
        <form action="/update_users" method="post">
            <label for="username">Usuário:</label>
            <input type="text" name="username" required>
            <label for="max_visits">Max Acessos:</label>
            <input type="number" name="max_visits" required>
            <button type="submit">Salvar</button>
        </form>
        <a href="/logout">Sair</a>
    </body>
    </html>
    ''')

@app.route('/admin_login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username == admin_username and password == admin_password:
            session['username'] = username
            return redirect(url_for('admin_panel'))
        else:
            return "Login inválido!"

    return '''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Login Administrativo</title>
    </head>
    <body>
        <h1>Login Administrativo</h1>
        <form method="POST">
            <input type="text" name="username" placeholder="Usuário" required>
            <input type="password" name="password" placeholder="Senha" required>
            <button type="submit">Entrar</button>
        </form>
    </body>
    </html>
    '''

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('admin_login'))

@app.route('/update_users', methods=['POST'])
@admin_required
def update_users():
    username = request.form['username']
    max_visits = int(request.form['max_visits'])
    
    if username in allowed_users:
        allowed_users[username]['max_visits'] = max_visits
    else:
        allowed_users[username] = {"visits": 0, "max_visits": max_visits}
    
    return redirect(url_for('admin_panel'))

if __name__ == '__main__':
    app.run(debug=True)
