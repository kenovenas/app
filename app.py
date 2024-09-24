from flask import Flask, request, jsonify, render_template_string
import secrets
import json

app = Flask(__name__)
application = app

# Caminho para o arquivo JSON que armazena os dados dos usuários
USERS_FILE = 'users.json'

# Função para carregar os dados dos usuários do arquivo JSON
def load_users():
    try:
        with open(USERS_FILE, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return {}

# Função para salvar os dados dos usuários no arquivo JSON
def save_users(users):
    with open(USERS_FILE, 'w') as file:
        json.dump(users, file, indent=4)

# Função para gerar uma chave aleatória
def generate_key():
    return secrets.token_hex(16)  # Gera uma chave hexadecimal de 16 bytes

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        username = request.form.get('username')
        users = load_users()

        if username in users:
            user_data = users[username]
            # Checa se o usuário ainda tem acessos disponíveis
            if user_data['visits'] < user_data['max_visits']:
                # Incrementa o número de acessos do usuário
                user_data['visits'] += 1
                save_users(users)  # Salva as alterações
                access_key = generate_key()
                remaining_access = user_data['max_visits'] - user_data['visits']
                return render_template_string('''
                <!DOCTYPE html>
                <html lang="en">
                <head>
                    <meta charset="UTF-8">
                    <meta name="viewport" content="width=device-width, initial-scale=1.0">
                    <title>Access Key</title>
                </head>
                <body>
                    <h1>Access Key</h1>
                    <p>Chave: {{ key }}</p>
                    <p>Acessos restantes: {{ remaining_access }}</p>
                </body>
                </html>
                ''', key=access_key, remaining_access=remaining_access)
            else:
                return "Acesso negado: número máximo de acessos atingido."
        else:
            return "Acesso negado: usuário não encontrado."
    
    # Formulário para o usuário inserir seu nome
    return render_template_string('''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Login</title>
    </head>
    <body>
        <h1>Obter Chave</h1>
        <form method="POST">
            <input type="text" name="username" placeholder="Digite seu nome de usuário" required>
            <button type="submit">Obter Chave</button>
        </form>
        <p>Entre em contato para ter acesso: <a href="https://t.me/Keno_venas" target="_blank">Keno Venas</a></p>
    </body>
    </html>
    ''')

@app.route('/admin_login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        # Logica de autenticação do admin (simplificada)
        if request.form['username'] == 'admin' and request.form['password'] == 'admin':
            return render_template_string('''
            <h1>Painel de Administração</h1>
            <form method="POST" action="/add_user">
                <h2>Adicionar Usuário</h2>
                <input type="text" name="username" placeholder="Nome do Usuário" required>
                <input type="number" name="max_visits" placeholder="Máximo de Acessos" required>
                <button type="submit">Adicionar Usuário</button>
            </form>
            ''')
        else:
            return "Login inválido"
    
    return render_template_string('''
    <form method="POST">
        <input type="text" name="username" placeholder="Usuário" required>
        <input type="password" name="password" placeholder="Senha" required>
        <button type="submit">Login</button>
    </form>
    ''')

@app.route('/add_user', methods=['POST'])
def add_user():
    username = request.form['username']
    max_visits = int(request.form['max_visits'])
    users = load_users()
    
    # Verifica se o usuário já existe
    if username not in users:
        users[username] = {
            "visits": 0,
            "max_visits": max_visits
        }
        save_users(users)
        return "Usuário adicionado com sucesso!"
    else:
        return "Usuário já existe."

if __name__ == '__main__':
    app.run(debug=True)
