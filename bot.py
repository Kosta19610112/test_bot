import os
from datetime import datetime, timedelta
from dotenv import load_dotenv
from flask import Flask, request
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
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
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hello!")

# Установка вебхука
async def set_webhook():
    WEBHOOK_URL = f"https://your-render-app-url.onrender.com/{BOT_TOKEN}"
    await application.bot.set_webhook(WEBHOOK_URL)

if __name__ == "__main__":
    # Регистрируем обработчик команды /start
    application.add_handler(CommandHandler("start", start))

    # Устанавливаем webhook
    asyncio.run(set_webhook())

    # Запускаем Flask-сервер
    app.run(host="0.0.0.0", port=10000)