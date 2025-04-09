from flask import Flask, request, jsonify
import telebot
import os
import requests
from datetime import datetime, timedelta
import pytz

OPENWEATHER_API_KEY = '1f30db42752361354d4cf1f02835861e'

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
#@bot.message_handler(commands=['start'])
#def send_welcome(message):
#    bot.reply_to(message, "Привет! Это простой бот.")

# Обработка всех остальных сообщений
#@bot.message_handler(func=lambda message: True)
#def echo_message(message):
#    bot.reply_to(message, message.text)





# ========== ТВОИ ФУНКЦИИ ==========

def get_weather(city):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={OPENWEATHER_API_KEY}&units=metric"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return data['main']['temp']
    return None

def get_forecast(city):
    url = f"http://api.openweathermap.org/data/2.5/forecast?q={city}&appid={OPENWEATHER_API_KEY}&units=metric"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        tomorrow = datetime.now() + timedelta(days=1)
        target_time = tomorrow.replace(hour=datetime.now().hour, minute=0, second=0, microsecond=0)
        for forecast in data['list']:
            forecast_time = datetime.strptime(forecast['dt_txt'], '%Y-%m-%d %H:%M:%S')
            if forecast_time.date() == target_time.date() and forecast_time.hour == target_time.hour:
                return forecast['main']['temp']
    return None

def get_local_time(city_timezone):
    timezone = pytz.timezone(city_timezone)
    return datetime.now(timezone).strftime('%Y-%m-%d %H:%M:%S')

# ========== ХЕНДЛЕРЫ ==========

@app.route('/')
def index():
    return "Привет! Это мой Telegram-бот. Он работает на Render."

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "Привет! Я могу показать текущее время, температуру и прогноз погоды в разных городах. Напишите /w.")

@bot.message_handler(commands=['w'])
def weather(message):
    current_time_moscow = get_local_time('Europe/Moscow')
    current_time_riga = get_local_time('Europe/Riga')

    moscow_temp = get_weather('Moscow')
    moscow_weather = f"Температура в Москве: {moscow_temp}°C" if moscow_temp is not None else "Не удалось получить данные о погоде в Москве."

    riga_temp = get_weather('Riga')
    riga_weather = f"Температура в Риге: {riga_temp}°C" if riga_temp is not None else "Не удалось получить данные о погоде в Риге."

    sevastopol_temp = get_weather('Sevastopol')
    sevastopol_weather = f"Температура в Севастополе: {sevastopol_temp}°C" if sevastopol_temp is not None else "Не удалось получить данные о погоде в Севастополе."

    moscow_forecast = get_forecast('Moscow')
    moscow_forecast_weather = f"Прогноз на завтра в Москве: {moscow_forecast}°C" if moscow_forecast is not None else "Не удалось получить прогноз погоды на завтра в Москве."

    riga_forecast = get_forecast('Riga')
    riga_forecast_weather = f"Прогноз на завтра в Риге: {riga_forecast}°C" if riga_forecast is not None else "Не удалось получить прогноз погоды на завтра в Риге."

    response = (
        f"Текущее время:\n"
        f"  - Москва: {current_time_moscow}\n"
        f"  - Рига: {current_time_riga}\n\n"
        f"{moscow_weather}\n"
        f"{riga_weather}\n"
        f"{sevastopol_weather}\n\n"
        f"{moscow_forecast_weather}\n"
        f"{riga_forecast_weather}"
    )
    bot.send_message(message.chat.id, response)










if __name__ == '__main__':
    WEBHOOK_URL = 'https://test-bot-klq6.onrender.com/' + BOT_TOKEN
    bot.remove_webhook()
    bot.set_webhook(url=WEBHOOK_URL)
    print(f"Приложение запущено на порту {os.environ.get('PORT')}")
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))