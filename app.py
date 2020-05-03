from flask import Flask
from flask import request
from flask import jsonify

import keyboard
from convert_for import Convert4

from rates_provider import getCurrencyRate
from rates_provider import convertCurrency
import realtby_parser
import requests
import json
import telebot
import re
bot = telebot.TeleBot('1218982080:AAFfj5mWdAMb4H6EEy1qlZ_7ug7eagM7Irw')

user_dict = {}

#class User:
#    def __init__(self, name):
#        self.name = name
#        self.age = None
#        self.sex = None

app = Flask(__name__)
#app.secret_key = "super secret key"

URL = 'https://api.telegram.org/bot1218982080:AAFfj5mWdAMb4H6EEy1qlZ_7ug7eagM7Irw/'
# register hooks 'https://api.telegram.org/bot1218982080:AAFfj5mWdAMb4H6EEy1qlZ_7ug7eagM7Irw/setWebhook?url=https://lovely-snail-15.telebit.io/'

#'https://api.telegram.org/bot1218982080:AAFfj5mWdAMb4H6EEy1qlZ_7ug7eagM7Irw/setWebhook?url=https://pytelegacurrency.azurewebsites.net/'

def write_json(data, filename='answer.json'):
    with open(filename, 'w') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def get_updates():
    url = URL + 'getUpdates'
    r = requests.get(url)
    write_json(r.json())
    return r.json()

def send_message(chat_id, text='bla bla bla'):
    url = URL + 'sendMessage'
    answer = {'chat_id': chat_id, 'text': text}
    r = requests.post(url, json=answer)
    return r.json()

def convertedToMoney(typed):
    if not typed:
        return False
    if re.match(r'^-?\d+(?:(\.|\,)\d+)?$', typed) is None:
        return False
    else:
        return True
#ROUTES
@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        r = request.get_json()
        if 'callback_query' in r:
            message = r['callback_query']['data']
            message_id = r['callback_query']['message']['message_id']
            from_user_id = r['callback_query']['from']['id']
            data = r['callback_query']['data']
            if data == 'byn2usd' or data == 'usd2byn' or data == 'byn2eur' or data == 'eur2byn' or data == 'byn2rub' or data == 'rub2byn':
                user_dict['prev_step'] = data
            else:
                pass
        else: 
            chat_id = r['message']['chat']['id']
            from_user_id = r['message']['from']['id']
            message = r['message']['text']
            message_id = r['message']['message_id']

        msg = message.lower()

        if 'hi' in msg:
            kbd = keyboard.getMainKeyboard()
            bot.send_message(from_user_id, 'Выбери операцию', reply_markup=kbd)
        elif 'converter' in msg:
            kbd = keyboard.getConverterKeyboard()
            bot.send_message(from_user_id, 'Что конвертируем?', reply_markup=kbd)
        elif 'byn2usd' == msg or 'usd2byn' == msg or 'byn2eur' == msg or 'eur2byn' == msg or 'byn2rub' == msg or 'rub2byn' == msg:
            bot.send_message(from_user_id, 'Укажите сумму')
        elif 'costm2' in msg:
            costm2 = realtby_parser.getRealtByCost()
            bot.send_message(from_user_id, costm2, parse_mode='Markdown')
        elif convertedToMoney(msg) and user_dict['prev_step'] != '':
            drct = user_dict['prev_step']
            if drct == '' or drct is None:
                bot.send_message(from_user_id, "Произошла ошибка на сервере")
            else:
                conversion_result = convertCurrency(msg.replace(',', '.'), drct)
                bot.send_message(from_user_id, conversion_result, parse_mode='Markdown')
        elif 'rates' in msg:
            kbd = keyboard.getRatesKeyboard()
            bot.send_message(from_user_id, 'Что вас интересует?', reply_markup=kbd)
        elif 'usd' == msg or 'eur' == msg or 'rub' == msg:
            rates = getCurrencyRate(msg)
            bot.send_message(from_user_id, rates, parse_mode='Markdown')
        else:
            bot.send_message(from_user_id, 'Функция в разработке...', parse_mode='Markdown')
        return jsonify(r)
    return '</h1>Bot welcomes you</h1>'

# Read about error handling
# https://stackoverflow.com/questions/46117104/except-connectionerror-or-timeouterror-not-working
#https://stackoverflow.com/questions/45048857/a-connection-attempt-failed-because-the-connected-party-did-not-properly-respond

@app.route('/ping')
def ping():
    return 'pong'

#MAIN
def main():
    pass

if __name__ == '__main__':
    app.run()
