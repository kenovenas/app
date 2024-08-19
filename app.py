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
def home():
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
        body {
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            height: 100vh;
            margin: 0;
            position: relative;
            font-family: Arial, sans-serif;
        }
        .header-banner {
            width: 100%;
            background-color: #ffcc00;
            padding: 10px;
            text-align: center;
            color: #0000ff;
            font-size: 18px;
            font-weight: bold;
            position: absolute;
            top: 0;
            left: 0;
            box-shadow: 0 2px 4px rgba(0,0,0,0.2);
        }
        .header-banner a {
            color: #0000ff;
            text-decoration: none;
        }
        .author {
            position: absolute;
            top: 50px; /* Ajuste conforme necessário */
            left: 10px;
            color: #000;
            font-size: 18px;
        }
        .banner-telegram {
            position: absolute;
            top: 50px; /* Ajuste conforme necessário */
            right: 10px;
            background-color: #0088cc;
            padding: 10px;
            border-radius: 5px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.2);
        }
        .banner-telegram a {
            color: #ffcc00;
            text-decoration: none;
            font-weight: bold;
        }
        .content {
            text-align: center;
            margin-top: 80px; /* Ajuste conforme necessário para dar espaço ao banner no topo */
        }
    </style>
</head>
<body>
    <div class="header-banner">
        <a href="https://crypto-faucets.netlify.app" target="_blank">Clique aqui para mais script!!!</a>
    </div>
    <div class="author">Autor = Keno Venas</div>
    <div class="banner-telegram">
        <a href="https://t.me/+Mns6IsONSxliZDkx" target="_blank">Grupo do Telegram</a>
    </div>
    <div class="content">
        <h1>Access Key</h1>
        <p>{key_data["key"]}</p>
    </div>

    <!-- Script da Hydro -->
    <script id="hydro_config" type="text/javascript">
        window.Hydro_tagId = "ab51bfd4-d078-4c04-a17b-ccfcfe865175";
    </script>
    <script id="hydro_script" src="https://track.hydro.online/"></script>
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
