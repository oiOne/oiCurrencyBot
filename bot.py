import telebot
from telebot import types
import config
import requests
from datetime import datetime
import json

bot = telebot.TeleBot(config.TOKEN)

def showCurrencyButtons(message):
    if message.text.lower() == 'hi' or message.text.lower() == '/hi':
        bot.send_message(message.from_user.id, f'Привет, {message.from_user.first_name}!')
        keyboard = types.InlineKeyboardMarkup()
        key_usd = types.InlineKeyboardButton(text='USD', callback_data='usd')
        keyboard.add(key_usd)
        key_eur = types.InlineKeyboardButton(text='EUR', callback_data='eur')
        keyboard.add(key_eur)
        key_rub = types.InlineKeyboardButton(text='RUB', callback_data='rub')
        keyboard.add(key_rub)
        bot.send_message(message.from_user.id, ' Выбери курс интересующей тебя валюты!', reply_markup=keyboard)
 
def handleNBRBResponse(resposneNBRB):
    jsonObj = json.loads(resposneNBRB)
    date = datetime.today().strftime("%d %B")
    abbr = jsonObj["Cur_Abbreviation"]
    rate = jsonObj["Cur_OfficialRate"]
    curScale = jsonObj["Cur_Scale"]
    if curScale > 1:
        return f'Курс *{abbr}* на {date} : {rate} за {curScale} {jsonObj["Cur_Name"]}'
    else : 
        return f'Курс *{abbr}* на {date} : {rate}'

@bot.callback_query_handler(func=lambda call: True)
def iq_callback(call):
    if call.data == 'usd' or call.data == 'eur' or call.data == 'rub':
        bot.answer_callback_query(call.id)
        rate = getCurrencyNBRB(call.data)
        bot.send_message(call.message.chat.id, rate, parse_mode='Markdown')
    else : 
       return 

def getCurrencyNBRB(currency_code):
    if currency_code.lower() == "hi" or currency_code.lower() == "/hi":
        return
    elif currency_code.lower() != "usd" and currency_code.lower() != "eur" and currency_code.lower() != "rub":
        return 'Напиши \'/hi\' или \'usd\' или \'eur\' или \'rub\'' 
    else:
        uri = 'https://www.nbrb.by/api/exrates/rates/'+ currency_code +'?parammode=2'
        response = requests.get(uri)
        if response.status_code == 200:
            print('Success!')
            responseContent = handleNBRBResponse(response.content)
            return responseContent
        elif response.status_code == 404:
            print('Not Found.')
            return 'Not Found'

@bot.message_handler(content_types=['text'])
def blabla(message):
    showCurrencyButtons(message)
    msg = getCurrencyNBRB(message.text)
    bot.send_message(message.chat.id, msg, parse_mode='Markdown')

#RUN
bot.polling(none_stop=True)