from flask import Flask, request
import requests

app = Flask(__name__)

TOKEN = 'YOUR_TELEGRAM_BOT_TOKEN'

@app.route(f'/{TOKEN}', methods=['POST'])
def respond():
    update = request.get_json()
    message = update.get('message', {}).get('text', '')
    chat_id = update.get('message', {}).get('chat', {}).get('id')

    # Простая логика ответа
    if message.lower() == 'привет':
        send_message(chat_id, 'Привет!')
    else:
        send_message(chat_id, 'Я понимаю только "привет"')
    
    return 'ok'

def send_message(chat_id, text):
    url = f'https://api.telegram.org/bot{TOKEN}/sendMessage'
    payload = {'chat_id': chat_id, 'text': text}
    requests.post(url, json=payload)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)