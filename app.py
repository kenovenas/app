from flask import Flask, request, jsonify, render_template 
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
            body {{
                display: flex;
                justify-content: center;
                align-items: center;
                height: 100vh;
                margin: 0;
            }}
            .content {{
                text-align: center;
            }}
            .author {{
                position: absolute;
                top: 10px;
                left: 10px;
            }}
        </style>
    </head>
    <body>
        <div class="author">Autor = Keno Venas</div>
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

if __name__ == 'main':
    #//app.run(host='127.0.0.1', port=5000)
    app.run(debug=true)
