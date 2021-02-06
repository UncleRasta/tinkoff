import requests
import json
import pandas as pd
from datetime import datetime
from openapi_client import openapi

from flask import Flask
from flask_sslify import SSLify
from flask import request
from pathlib import Path
from dotenv import load_dotenv
import os
import re

env_path = Path('.') / '.env'

load_dotenv(dotenv_path=env_path)

tink_token = os.environ['TINK_TOKEN']
tg_token = os.environ['TG_TOKEN']

app = Flask(__name__)
sslify = SSLify(app)

URL = 'https://api.telegram.org/' + tg_token

client = openapi.api_client(tink_token)

def get_portfolio():
    pf = client.portfolio.portfolio_currencies_get()
    for i in pf.payload.positions:
        print(i.name)
        print(i.average_position_price)
        print(i.expected_yield)

def parse_text(text):
    pattern = r'/\w+'
    crypto = re.search(pattern, text).group()
    return crypto[1:]

def send_message(chat_id, text):
    url = URL + 'sendMessage'
    answer = {'chat_id': chat_id, 'text': text}
    r = requests.post(url, json=answer)
    return r.json()

def provide_keyboard(chat_id):
    url = URL + 'sendMessage'
    answer = {'chat_id': chat_id, "text": "Here are the options:",
      "reply_markup": {
        "keyboard": [
      [
        {"text": "Portfolio"},
        {"text": "Anomalies"},
        {"text": "Operations"}
      ]]}}

    requests.post(url, json=answer)

def remove_keyboard(chat_id, text):
    url = URL + 'sendMessage'
    answer = {'chat_id': chat_id, "text": text,
      "reply_markup": {
        "remove_keyboard": True}}

    requests.post(url, json=answer)

@app.route('/', methods = ['POST', 'GET'])
def index():
    if request.method == 'POST':
        r = request.get_json()
        chat_id = r['message']['chat']['id']
        message = r['message']['text']

        if '/start' in message.lower():
            provide_keyboard(chat_id)

        elif message.lower() ==  '/help':
            send_message(chat_id, text = "Here is the list of operations")

        elif 'thank you' in message.lower():
            send_message(chat_id, text = 'My pleasure!')

        else:
            send_message(chat_id, text = "Sorry, can't understand you, I'm just an exchange bot but i'm constantly imporving! For now, try again, please.")


    return '<h1>Bot welcomes you</h1>'

if __name__ == '__main__':
    #main()
    app.run()
