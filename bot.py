import os
import telebot
from flask import Flask, request
from dotenv import load_dotenv

load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")
WEBHOOK_URL = os.getenv("WEBHOOK_URL")

bot = telebot.TeleBot(BOT_TOKEN)
app = Flask(__name__)

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "Привет! Я бот на вебхуках 🚀")

@bot.message_handler(func=lambda message: True)
def echo_all(message):
    bot.reply_to(message, message.text)

@app.route('/' + BOT_TOKEN, methods=['POST'])
def webhook():
    json_str = request.get_data().decode('utf-8')
    update = telebot.types.Update.de_json(json_str)
    bot.process_new_updates([update])
    return '', 200

@app.route('/')
def index():
    return 'Бот работает.'

if __name__ == '__main__':
    bot.remove_webhook()
    bot.set_webhook(url=f"{WEBHOOK_URL}/{BOT_TOKEN}")
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
