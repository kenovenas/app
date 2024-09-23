from flask import Flask, request, jsonify
import secrets
import time

app = Flask(__name__)
application = app

# Armazenamento para chave e seu timestamp
key_data = {
    "key": None,
    "timestamp": None
}

# Lista de IPs permitidos
allowed_ips = {"127.0.0.1"}  # Substitua pelo seu IP reverso correto

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

# Função para verificar se o IP está na lista de permitidos
def is_ip_allowed(ip):
    return ip in allowed_ips

@app.route('/')
def home():
    # Obtém o IP do usuário
    user_ip = request.environ.get('HTTP_X_REAL_IP', request.remote_addr)
    
    # Exibe o IP no console e na página
    print(f"IP do usuário: {user_ip}")  # Log do IP do usuário
    print(f"IPs permitidos: {allowed_ips}")  # Log dos IPs permitidos

    # Mostra o IP no navegador para verificação
    if not is_ip_allowed(user_ip):
        return f'''
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Acesso Negado</title>
            <style>
                body {{
                    display: flex;
                    justify-content: center;
                    align-items: center;
                    height: 100vh;
                    margin: 0;
                    text-align: center;
                }}
                .button {{
                    background-color: #0088cc;
                    color: white;
                    padding: 10px 20px;
                    border: none;
                    border-radius: 5px;
                    cursor: pointer;
                    text-decoration: none;
                }}
            </style>
        </head>
        <body>
            <h1>Acesso Negado</h1>
            <p>Entre em contato</p>
            <a href="https://t.me/Keno_venas" class="button">Keno Venas</a>
            <p>Seu IP: {user_ip}</p>
        </body>
        </html>
        '''

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
        </style>
    </head>
    <body>
        <div class="author">Autor = Keno Venas</div>
        <div class="banner-telegram">
            <a href="https://t.me/+Mns6IsONSxliZDkx" target="_blank">Grupo do Telegram</a>
        </div>
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
