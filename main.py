import os
import requests
from flask import Flask
import telebot
import threading

# Credenciales desde las variables de entorno de Render
TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
LAPAK_KEY = os.environ.get("LAPAK_SECRET_KEY")

bot = telebot.TeleBot(TOKEN)

# Servidor web falso para cumplir con el requisito de puertos de Render
app = Flask(_name_)


@app.route("/")
def home():
  return "¡El bot de recargas de Tobirama JC está activo y funcionando!"


def run_flask():
  port = int(os.environ.get("PORT", 10000))
  app.run(host="0.0.0.0", port=port)


# --- COMANDO DE BIENVENIDA ---
@bot.message_handler(commands=["start"])
def send_welcome(message):
  bot.reply_to(
      message,
      "¡Qué onda! 🎮💎 Bienvenido al sistema de recargas de **Tobirama"
      " JC**.\n\nPara iniciar una recarga, usa el comando:\n`/recargar"
      " ID_JUGADOR PRODUCTO`\n\nEjemplo: /recargar 123456789 diamantes_100",
      parse_mode="Markdown",
  )


# --- COMANDO PARA PROCESAR RECARGAS ---
@bot.message_handler(commands=["recargar"])
def procesar_recarga(message):
  try:
    # Dividimos el mensaje para extraer el ID y el producto
    partes = message.text.split()
    if len(partes) < 3:
      bot.reply_to(
          message,
          "⚠️ *Formato incorrecto.*\nUsa: /recargar ID_JUGADOR PRODUCTO",
          parse_mode="Markdown",
      )
      return

    player_id = partes[1]
    product = partes[2]

    bot.reply_to(
        message,
        f"🔄 Procesando recarga para el ID: {player_id}...",
        parse_mode="Markdown",
    )

    # AQUÍ PUEDES INTEGRAR TU LLAMADA A LA API DE LAPAKGAMING
    # Usando LAPAK_KEY para autenticar las peticiones de forma segura.
    # Ejemplo de headers: headers = {"Authorization": f"Bearer {LAPAK_KEY}"}

    # Respuesta simulada de éxito (puedes adaptarla cuando conectes la API final)
    bot.reply_to(
        message,
        f"✅ ¡Solicitud recibida con éxito!\n\n*🎮 ID de Jugador:*"
        f" {player_id}\n*📦 Producto:* {product}\n*💼 Estado:* En cola de"
        f" despacho.",
        parse_mode="Markdown",
    )

  except Exception as e:
    bot.reply_to(message, f"❌ Error interno al procesar la recarga: {str(e)}")


if _name_ == "_main_":
  # Arrancamos Flask en un hilo secundario para abrir el puerto web
  t = threading.Thread(target=run_flask)
  t.start()

  # Arrancamos el bot de Telegram en el hilo principal
  print("Bot iniciado y escuchando...")
  bot.infinity_polling()
