from telethon.sync import TelegramClient

api_id = 20225004
api_hash = '8f4c78e858658cd2aa21967a087bf819'

with TelegramClient('session', api_id, api_hash) as client:
    print("Login concluído e sessão criada.")
