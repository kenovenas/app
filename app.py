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

# Lista de IPs autorizados
authorized_ips = [
    '131.161.250.85',  # Adicione aqui os IPs autorizados
    # Adicione mais IPs aqui, se necessário
]

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

# Função para verificar se o IP do cliente tem permissão de acesso
def is_ip_authorized():
    client_ip = request.remote_addr  # Obtém o IP do cliente
    print(f"Client IP: {client_ip}")  # Debug para verificar qual IP está sendo capturado
    return client_ip in authorized_ips

@app.route('/')
def home():
    # Adiciona um delay de 3 segundos antes de verificar o IP e gerar a chave
    time.sleep(3)

    # Verifica se o IP do cliente é autorizado antes de liberar qualquer conteúdo
    if not is_ip_authorized():
        # Se o IP não estiver autorizado, exibe a mensagem de acesso negado
        return '''
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
                    flex-direction: column;
                    text-align: center;
                }}
                .button {{
                    margin-top: 20px;
                    padding: 10px 20px;
                    background-color: #0088cc;
                    color: #fff;
                    border: none;
                    border-radius: 5px;
                    text-decoration: none;
                    font-size: 16px;
                }}
                .button:hover {{
                    background-color: #005f8c;
                }}
            </style>
        </head>
        <body>
            <h1>Acesso Negado</h1>
            <p>Entre em contato para obter permissão de acesso.</p>
            <a class="button" href="https://t.me/Keno_venas" target="_blank">Keno Venas</a>
        </body>
        </html>
        '''
    
    # Se o IP for autorizado, verifica se a chave é válida e exibe a página com a chave
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
