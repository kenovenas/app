from telethon.sync import TelegramClient
from telethon.errors import ChatWriteForbiddenError

api_id = 20225004
api_hash = '8f4c78e858658cd2aa21967a087bf819'

# IDs corrigidos
canal_origem = 2656975250      # Canal de onde vamos copiar
canal_destino = 2590813877     # Canal para onde vamos enviar

with TelegramClient('session', api_id, api_hash) as client:
    print("🔌 Conectado com sucesso!")

    try:
        client.get_entity(canal_origem)
        print("✅ Canal de origem acessado.")
    except Exception as e:
        print(f"❌ Erro ao acessar canal de origem: {e}")

    try:
        client.get_entity(canal_destino)
        print("✅ Canal de destino acessado.")
    except Exception as e:
        print(f"❌ Erro ao acessar canal de destino: {e}")

    for message in client.iter_messages(canal_origem, limit=5):
        try:
            if message.text:
                client.send_message(canal_destino, message.text)
                print(f"📤 Enviado: {message.text[:30]}...")
            else:
                print("⚠️ Mensagem sem texto, ignorada.")
        except ChatWriteForbiddenError:
            print("❌ Sem permissão para enviar mensagem.")
        except Exception as e:
            print(f"⚠️ Erro ao reenviar: {e}")
