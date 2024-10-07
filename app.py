from flask import Flask, request, jsonify, render_template_string
import secrets
import time

app = Flask(__name__)
application = app

# Armazenamento para chave, timestamp e usuários permitidos
key_data = {
    "key": None,
    "timestamp": None
}

# Usuários permitidos
allowed_users = {
    "pstfr", "emda", "wndrsn", "thglm", "emrsnc", "cslxnd", 
    "wlsn", "edrd", "vttb", "tmmz", "wltr", "crtntt", "rcrd", 
    "ndrtx", "vttbt", "mrn", "rflcr", "cnt", "wbss", "zr1", "nbsbt"
}  # Adicione os usuários permitidos aqui

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

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        username = request.form.get('username')
        if username in allowed_users:  # Verifica se o usuário está na lista permitida
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
                        flex-direction: column;
                        background-color: #f4f4f4;
                    }}
                    .content {{
                        text-align: center;
                        background-color: #007bff;
                        padding: 20px;
                        border-radius: 10px;
                        color: white;
                    }}
                </style>
            </head>
            <body>
                <div class="content">
                    <h1>Sua Chave de Acesso</h1>
                    <p>{key_data["key"]}</p>
                </div>
            </body>
            </html>
            ''')
        else:
            return "Acesso negado"

    # Tela de login com o banner modificado
    return '''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Login</title>
        <style>
            body {{
                display: flex;
                justify-content: center;
                align-items: center;
                height: 100vh;
                margin: 0;
                background-color: #f4f4f4;
            }}
            .login-container {{
                background-color: #007bff;
                padding: 30px;
                border-radius: 10px;
                text-align: center;
                color: white;
                box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
                width: 300px;
            }}
            .login-container input[type="text"] {{
                padding: 10px;
                margin-top: 10px;
                border: none;
                border-radius: 5px;
                width: 100%;
                box-sizing: border-box;
                font-size: 16px;
            }}
            .login-container button {{
                margin-top: 15px;
                padding: 10px 20px;
                border: none;
                border-radius: 5px;
                background-color: #28a745;
                color: white;
                font-size: 16px;
                cursor: pointer;
                width: 100%;
            }}
            .login-container button:hover {{
                background-color: #218838;
            }}
            .login-container p {{
                margin-top: 15px;
                font-size: 14px;
                color: white;
            }}
            .login-container a {{
                color: #ffc107;
                text-decoration: none;
            }}
            .login-container a:hover {{
                text-decoration: underline;
            }}
        </style>
    </head>
    <body>
        <div class="login-container">
            <h1>Digite seu usuário</h1>
            <form method="POST">
                <input type="text" name="username" placeholder="Usuário" required>
                <button type="submit">Acessar</button>
            </form>
            <p>Para ter acesso entre em contato.</p>
            <p><a href="https://t.me/Keno_venas" target="_blank">Keno Venas</a></p>
            <p><a href="https://t.me/+Mns6IsONSxliZDkx" target="_blank">Grupo do Telegram</a></p>
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
