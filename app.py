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
    "wlsn", "edrd", "vttb", "tmmz", "wltr", "crtntt", 
    "wndrsn", "rcrd", "ndrtx", "vttbt", "mrn", "rflcr", 
    "cnt", "wbss", "zr1", "nbsbt"
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

# Rota da página de login
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
        </style
