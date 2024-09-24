from flask import Flask, request, jsonify, render_template_string
import secrets
import json
import os

app = Flask(__name__)
application = app

# Nome do arquivo JSON onde os usuários são armazenados
USERS_FILE = 'users.json'

# Função para carregar usuários do arquivo JSON
def load_users():
    if os.path.exists(USERS_FILE):
        with open(USERS_FILE, 'r') as f:
            return json.load(f)
    return {}

# Função para salvar usuários no arquivo JSON
def save_users(users):
    with open(USERS_FILE, 'w') as f:
        json.dump(users, f, indent=4)

# Carrega usuários ao iniciar o servidor
users = load_users()

# Rota para o painel de administração
@app.route('/admin_login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if username == 'admin' and password == 'admin':  # Autenticação simples
            return render_template_string('''
                <h1>Painel de Administração</h1>
                <form method="POST" action="/add_user">
                    Nome do Usuário: <input type="text" name="username" required>
                    Máximo de Acessos: <input type="number" name="max_visits" required>
                    <button type="submit">Adicionar Usuário</button>
                </form>
                <br>
                <form method="POST" action="/view_users">
                    <button type="submit">Ver Usuários</button>
                </form>
            ''')
    return render_template_string('''
        <h1>Login do Administrador</h1>
        <form method="POST">
            Usuário: <input type="text" name="username" required>
            Senha: <input type="password" name="password" required>
            <button type="submit">Entrar</button>
        </form>
    ''')

# Rota para adicionar um usuário
@app.route('/add_user', methods=['POST'])
def add_user():
    new_username = request.form.get('username')
    max_visits = int(request.form.get('max_visits'))

    # Verifica se o usuário já existe
    if new_username in users:
        return "Usuário já existe!", 400

    # Adiciona novo usuário sem redefinir os existentes
    users[new_username] = {"visits": 0, "max_visits": max_visits}
    save_users(users)

    return "Usuário adicionado com sucesso!", 200

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        username = request.form.get('username')
        if username in users:
            user = users[username]
            if user['visits'] < user['max_visits']:
                # Gera a chave
                key = secrets.token_hex(16)
                user['visits'] += 1
                save_users(users)  # Salva as alterações
                return f'Chave: {key}, Acessos restantes: {user["max_visits"] - user["visits"]}'
            else:
                return "Acesso negado! Limite de visitas atingido.", 403
        return "Usuário não encontrado!", 404

    return '''
        <form method="POST">
            Insira o nome de usuário: <input type="text" name="username" required>
            <button type="submit">Obter Chave</button>
        </form>
    '''

# Rota para ver usuários
@app.route('/view_users', methods=['POST'])
def view_users():
    user_list = '<h1>Usuários Cadastrados</h1><ul>'
    for username, details in users.items():
        user_list += f'<li>{username}: {details["max_visits"]} acessos máximos, {details["visits"]} acessos utilizados</li>'
    user_list += '</ul><a href="/admin_login">Voltar</a>'
    return user_list

if __name__ == '__main__':
    app.run(debug=True)
