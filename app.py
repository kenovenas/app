from flask import Flask, request, jsonify, render_template_string
import secrets
import time

app = Flask(__name__)
application = app

# Armazenamento para chave e seu timestamp
key_data = {
    "key": None,
    "timestamp": None
}

# Lista de usuários permitidos
allowed_users = ["pstfr", 
                 "emda",
                 "wndrsn",
                "thglm",
                "emrsnc",
                "cslxnd",
                "wlsn",
                "edrd",
                "vttb",
                "tmmz",
                "wltr",
                 "crtntt",
                 "wndrsn",
                 "rcrd",
                 "ndrtx",
                 "vttbt",
                 "mrn",
                 "rflcr",
                 "cnt",
                 "wbss",
                 "zr1",
                 "nbsbt",
                 "mxchk",
                 "pdrrm",
                 "hll",
                 "mro",
                 "hmd",
                 "mrclm",
                 "mxwll",
                 "kauan"]

# Função para gerar uma chave aleatória
def generate_key():
    return secrets.token_hex(16)  # Gera uma chave hexadecimal de 16 bytes

# Função para verificar se a chave ainda é válida
def is_key_valid():
    if key_data["key"] and key_data["timestamp"]:
        current_time = time.time()
        # Verifica se a chave ainda é válida (5 minutos = 300 segundos)
        if current_time - key_data["timestamp"] <= 300:
            return True
    return False

@app.route('/')
def login():
    return '''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Login</title>
        <style>
            body {
                display: flex;
                justify-content: center;
                align-items: center;
                height: 100vh;
                margin: 0;
                background-color: #f4f4f9;
            }
            .login-container {
                text-align: center;
                padding: 20px;
                border-radius: 10px;
                box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
                background-color: white;
                width: 300px;
                display: flex;
                flex-direction: column;
                align-items: center;
            }
            .login-container h1 {
                margin-bottom: 20px;
            }
            .login-container form {
                display: flex;
                flex-direction: column;
                width: 100%;
            }
            .login-container input {
                padding: 10px;
                margin-bottom: 10px;
                width: 100%;
                border: 1px solid #ccc;
                border-radius: 5px;
            }
            .login-container button {
                padding: 10px 20px;
                background-color: #0088cc;
                color: white;
                border: none;
                border-radius: 5px;
                cursor: pointer;
                width: 100%;
            }
            .login-container button:hover {
                background-color: #005f99;
            }
            .contact {
                margin-top: 20px;
            }
            .author-link {
                color: #0088cc;
                text-decoration: none;
                font-weight: bold;
            }
            .telegram-group {
                margin-top: 10px;
            }
            .telegram-group a {
                color: #ffcc00;
                text-decoration: none;
                font-weight: bold;
            }
        </style>
    </head>
    <body>
        <div class="login-container">
            <h1>Login</h1>
            <form action="/login" method="post">
                <input type="text" id="username" name="username" placeholder="Usuário" required><br>
                <button type="submit">Login</button>
            </form>
            <div class="contact">
                <p>Para acessar entre em contato:</p>
                <a class="author-link" href="https://t.me/Keno_venas" target="_blank">Keno Venas</a>
            </div>
            <div class="telegram-group">
                <p>Grupo do Telegram:</p>
                <a href="https://t.me/+Mns6IsONSxliZDkx" target="_blank">Crypto Faucets</a>
            </div>
        </div>
    </body>
    </html>
    '''



# Rota para autenticação
@app.route('/login', methods=['POST'])
def authenticate():
    username = request.form['username']
    if username in allowed_users:
        # Redireciona para a página de exibição da chave com o parâmetro logged_in
        return redirect(url_for('home', logged_in=True))
    else:
        return '''
        <h1>Usuário não autorizado!</h1>
        <a href="/">Voltar para o login</a>
        '''

# Rota da página que exibe a chave, acessível apenas após login
@app.route('/home')
def home():
    # Verifica se o parâmetro logged_in está presente na requisição
    logged_in = request.args.get('logged_in', None)
    if logged_in != 'True':  # Redireciona para o login se o parâmetro não for encontrado
        return redirect(url_for('login'))

    if not is_key_valid():
        key_data["key"] = generate_key()
        key_data["timestamp"] = time.time()

    return f'''
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
        </style>
    </head>
    <body>
        <div class="author">Autor: Keno Venas</div>
        <div class="content">
            <h1>Access Key</h1>
            <p>{key_data["key"]}</p>
        </div>
    </body>
    </html>
    '''

@app.route('/validate', methods=['POST'])
def validate_key():
    data = request.get_json()
    if 'key' in data:
        if data['key'] == key_data['key'] and is_key_valid():
            return jsonify({"valid": True}), 200
    return jsonify({"valid": False}), 401

if __name__ == '__main__':
    app.run(debug=True)
