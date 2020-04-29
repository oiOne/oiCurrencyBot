import telebot
import config
import requests
from datetime import datetime
import json
import locale

bot = telebot.TeleBot(config.TOKEN)
# export LC_ALL='ru-RU.UTF-8'
# locale.setlocale(locale.LC_ALL,'ru_RU.UTF-8')

def handleNBRBResponse(resposneNBRB):
    jsonObj = json.loads(resposneNBRB)
    # date = datetime.strptime(jsonObj["Date"], "yyyy-MM-dd'T'HH:mm:ss")
    date = datetime.today().strftime("%d %B")
    abbr = jsonObj["Cur_Abbreviation"]
    rate = jsonObj["Cur_OfficialRate"]
    return f'Курс *{abbr}* на {date} : {rate}'
def getCurrencyNBRB(currency_code):
    print(currency_code)
    if currency_code.lower() != "usd" and currency_code.lower() != "eur":
        return currency_code
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
    msg = getCurrencyNBRB(message.text)
    print(msg)
    bot.send_message(message.chat.id, msg, parse_mode='Markdown')





#RUN
bot.polling(none_stop=True)