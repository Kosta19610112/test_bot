from flask import Flask, request, jsonify
import telebot
import os


# Инициализация Flask приложения
app = Flask(__name__)

# Ваш токен бота
BOT_TOKEN = '7649841006:AAH9H1G18v6X_nMYZ_7IeaVK1TDyP9m_7nw'
bot = telebot.TeleBot(BOT_TOKEN)

# Установка вебхука
@app.route('/' + BOT_TOKEN, methods=['POST'])
def webhook():
    json_update = request.get_json()
    update = telebot.types.Update.de_json(json_update)
    bot.process_new_updates([update])
    return jsonify({'status': 'ok'})

# Простая команда /start
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Привет! Это простой бот.")

# Обработка всех остальных сообщений
@bot.message_handler(func=lambda message: True)
def echo_message(message):
    bot.reply_to(message, message.text)


if __name__ == '__main__':
    WEBHOOK_URL = 'https://test-bot-klq6.onrender.com/' + BOT_TOKEN
    bot.remove_webhook()
    bot.set_webhook(url=WEBHOOK_URL)
    print(f"Приложение запущено на порту {os.environ.get('PORT')}")
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))