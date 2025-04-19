from telethon.sync import TelegramClient

# Substitua com sua API ID e API Hash
api_id = 20225004
api_hash = '8f4c78e858658cd2aa21967a087bf819'

# Substitua com o seu número de telefone (ex: +5511999999999) ou token de bot
phone_number = input("Digite seu número de telefone com o código do país: ")

# Inicia sessão com o nome 'session'
with TelegramClient('session', api_id, api_hash) as client:
    print("Conectado com sucesso!")

    # Tenta se conectar ao canal com o link fornecido
    link_do_canal = "https://t.me/+91IjIh9b6VllMjIx"  # Substitua pelo link do canal desejado
    try:
        # Junte-se ao canal usando o link
        channel = client.get_entity(link_do_canal)
        print(f"Canal encontrado: {channel.title}")
        print(f"ID do canal: {channel.id}")
    except Exception as e:
        print(f"Erro ao acessar o canal: {e}")
