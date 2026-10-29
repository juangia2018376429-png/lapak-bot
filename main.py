import os
import time
import requests
import telebot

# Las credenciales se leen de forma segura del entorno
TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
LAPAK_SECRET_KEY = os.environ.get("LAPAK_SECRET_KEY")

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=["recargar"])
def handle_recharge(message):
  try:
    # Comando esperado: /recargar <user_id> <product_code>
    # Ejemplo: /recargar 522954046 FFLATAM100-S136-mx
    args = message.text.split()
    if len(args) < 3:
      bot.reply_to(
          message,
          "❌ *Formato incorrecto.*\nUsa:\n`/recargar <ID_JUEGO>`"
          " <CODIGO_PAQUETE>",
          parse_mode="Markdown",
      )
      return

    user_id = args[1]
    product_code = args[2]

    # Generar un partner_reference_id único basado en milisegundos
    partner_ref_id = f"TX-{int(time.time() * 1000)}"

    # Petición a la API de producción de Lapakgaming
    url = "https://api.lapakgaming.com/api/order"
    headers = {
        "Authorization": f"Bearer {LAPAK_SECRET_KEY}",
        "Content-Type": "application/json",
    }
    payload = {
        "user_id": user_id,
        "count_order": 1,
        "product_code": product_code,
        "partner_reference_id": partner_ref_id,
    }

    bot.reply_to(
        message,
        f"⏳ Procesando recarga de diamantes para el ID {user_id}...",
        parse_mode="Markdown",
    )

    response = requests.post(url, json=payload, headers=headers)
    res_data = response.json()

    if response.status_code == 200 and res_data.get("code") == "SUCCESS":
      data = res_data.get("data", {})
      tid = data.get("tid", "N/A")
      product_name = data.get("product_name", product_code)
      total_price = data.get("total_price", "N/A")

      respuesta_texto = (
          f"✅ *¡Recarga Exitosa!*\n\n"
          f"📦 *Producto:* {product_name}\n"
          f"👤 *ID de Usuario:* {user_id}\n"
          f"🧾 *TID:* {tid}\n"
          f"🔢 *Referencia:* {partner_ref_id}\n"
          f"💰 *Costo:* {total_price}"
      )
    else:
      respuesta_texto = (
          f"❌ *Error al procesar:*\njson\n{response.text}\n"
      )

    bot.reply_to(message, respuesta_texto, parse_mode="Markdown")

  except Exception as e:
    bot.reply_to(message, f"⚠️ Error interno en el bot: {str(e)}")


if __name__ == "__main__":
  print("Bot iniciado y escuchando...")
  bot.infinity_polling()
