import os
from datetime import datetime, timedelta
from dotenv import load_dotenv
from flask import Flask, request
from telegram import Update
from telegram.ext import Application, CommandHandler, CallbackContext
import asyncio

# Загружаем переменные окружения
load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")

# Создаем экземпляр Flask-приложения
app = Flask(__name__)

# Создаем приложение Telegram
application = Application.builder().token(BOT_TOKEN).build()

# Маршрут для вебхука
@app.route(f"/{BOT_TOKEN}", methods=["POST"])
async def webhook():
    update_data = request.get_json(force=True)
    update = Update.de_json(update_data, application.bot)
    await application.update_queue.put(update)
    return "ok"

# Обработчик команды /start
async def start(update: Update, context: CallbackContext):
    await update.message.reply_text("Hello!")

# Обработчик команды /w (заглушка)
async def w_command(update: Update, context: CallbackContext):
    await update.message.reply_text("Это заглушка для команды /w")

# Установка вебхука
async def set_webhook():
    WEBHOOK_URL = f"https://test-bot-klq6.onrender.com/{BOT_TOKEN}"
    await application.bot.set_webhook(WEBHOOK_URL)

if __name__ == "__main__":
    # Регистрируем обработчики команд
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("w", w_command))  # Добавляем обработчик для /w

    # Устанавливаем webhook
    asyncio.run(set_webhook())

    # Запускаем Flask-сервер
    app.run(host="0.0.0.0", port=10000)