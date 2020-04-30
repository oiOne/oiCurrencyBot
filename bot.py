import telebot
from telebot import types
import requests
from datetime import datetime
import json

import os

tkn = os.environ.get("TOKEN", default="1218982080:AAGF01PcFTYBfsvNZhT3n0_Px87k98ke3P0")
bot = telebot.TeleBot(tkn)

# !!!! keyboards
def getRatesKeyboard():
    ratesKB = types.InlineKeyboardMarkup()
    key_usd = types.InlineKeyboardButton(text='USD', callback_data='usd')
    ratesKB.add(key_usd)
    key_eur = types.InlineKeyboardButton(text='EUR', callback_data='eur')
    ratesKB.add(key_eur)
    key_rub = types.InlineKeyboardButton(text='RUB', callback_data='rub')
    ratesKB.add(key_rub)
    return ratesKB;

def getCurrencyConverterKeyboard():
    currencyConverterKB = types.InlineKeyboardMarkup()
    key_rates = types.InlineKeyboardButton(text='Курсы', callback_data='rates')
    currencyConverterKB.add(key_rates)
    key_converter = types.InlineKeyboardButton(text='Конвертер', callback_data='converter')
    currencyConverterKB.add(key_converter)
    return currencyConverterKB;

def getConverterOptions():
    ratesKB = types.InlineKeyboardMarkup()
    
    key_byn2usd = types.InlineKeyboardButton(text='BYN -> USD', callback_data='byn2usd')
    ratesKB.add(key_byn2usd)
    key_usd2byn = types.InlineKeyboardButton(text='USD -> BYN', callback_data='usd2byn')
    ratesKB.add(key_usd2byn)

    key_byn2eur = types.InlineKeyboardButton(text='BYN -> EUR', callback_data='byn2eur')
    ratesKB.add(key_byn2eur)
    key_eur2byn = types.InlineKeyboardButton(text='EUR -> BYN', callback_data='eur2byn')
    ratesKB.add(key_eur2byn)

    return currencyConverterKB;

def showMainButtons(message):
    if message.text.lower() == 'hi' or message.text.lower() == '/hi':
        bot.send_message(message.from_user.id, f'Привет, {message.from_user.first_name}!')
        kb = getCurrencyConverterKeyboard()
        bot.send_message(message.from_user.id, 'Выбери операцию', reply_markup=kb)
    else:
        bot.send_message(message.from_user.id, f'Опция в разработке')
 
#def showMainOptions(id, firstName):
#    kb = getCurrencyConverterKeyboard()
#    bot.send_message(id, f'Привет, {firstName}!')
#    bot.send_message(id, ' Выбери курс интересующей тебя валюты!', reply_markup=kb)

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

# here is place where we handle request from button click in chat
@bot.callback_query_handler(func=lambda call: True)
def iq_callback(call):
    if call.data == 'usd' or call.data == 'eur' or call.data == 'rub':
        bot.answer_callback_query(call.id)
        rate = getCurrencyNBRB(call.data)
        bot.send_message(call.message.chat.id, rate, parse_mode='Markdown')
    elif call.data == 'rates':
        bot.answer_callback_query(call.id)
        kb = getRatesKeyboard()
        bot.send_message(call.message.chat.id, 'Выбери курс интересующей тебя валюты!', reply_markup=kb)
    elif call.data == 'converter':
        bot.answer_callback_query(call.id)
        bot.send_message(call.message.chat.id, 'Опция в разработке')
        
        #kb = getConverterOptions()
        #bot.send_message(call.message.chat.id, 'Выбери конвертацию', reply_markup=kb)
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
    showMainButtons(message)
    msg = getCurrencyNBRB(message.text)
    bot.send_message(message.chat.id, msg, parse_mode='Markdown')

def RUN():
    bot.polling(none_stop=True)