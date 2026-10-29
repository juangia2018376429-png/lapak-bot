import os
from flask import Flask
import telebot
import threading

# Configuración del bot de Telegram
TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
bot = telebot.TeleBot(TOKEN)

# Servidor web falso para cumplir con los requisitos de Render
app = Flask(__name__)


@app.route("/")
def home():
  return "¡El bot de recargas está activo!"


def run_flask():
  port = int(os.environ.get("PORT", 10000))
  app.run(host="0.0.0.0", port=port)


# --- AQUÍ VAN TUS COMANDOS DEL BOT ---
@bot.message_handler(commands=["start", "recargar"])
def send_welcome(message):
  bot.reply_to(message, "¡Hola! Envía tu formato de recarga.")


# ------------------------------------

if __name__ == "__main__":
  # Arrancamos Flask en un hilo secundario para abrir el puerto web
  t = threading.Thread(target=run_flask)
  t.start()

  # Arrancamos el bot de Telegram en el hilo principal
  print("Bot iniciado y escuchando...")
  bot.infinity_polling()
