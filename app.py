from telethon.sync import TelegramClient

# Insira diretamente aqui:
api_id = 20225004
api_hash = '8f4c78e858658cd2aa21967a087bf819'

canal_origem = 2656975250
canal_destino = 2590813877

with TelegramClient('session', api_id, api_hash) as client:
    print("Conectado com sucesso!")
    for message in client.iter_messages(canal_origem, limit=5):
        if message.text:
            client.send_message(canal_destino, message.text)
            print(f"Mensagem enviada: {message.text[:30]}...")
