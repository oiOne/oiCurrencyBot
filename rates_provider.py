# rates provider consumes NB RB Api
import requests
from datetime import datetime, date, time
import json

rates_dict = {}

def getJustCurrencyRate(currency_code):
    uri = 'https://www.nbrb.by/api/exrates/rates/'+ currency_code +'?parammode=2'
    response = requests.get(uri)
    if response.status_code == 200:
        jsonObj = json.loads(response.content)
        rates_dict[currency_code+'_resp'] = response.content
        rate = jsonObj["Cur_OfficialRate"]
        return rate
    elif response.status_code == 404:
        return None

def update_all_rates():
    r_usd = getJustCurrencyRate('usd')
    r_eur = getJustCurrencyRate('eur')
    r_rub = getJustCurrencyRate('rub')
    rates_dict['usd'] = r_usd
    rates_dict['eur'] = r_eur
    rates_dict['rub'] = r_rub

def getPreselectedRates(code):
    if not code in rates_dict:
        update_all_rates()
    return rates_dict[code]

def handleResponse(resposneNBRB):
    jsonObj = json.loads(resposneNBRB)
    date = datetime.today().strftime("%d %B")
    abbr = jsonObj["Cur_Abbreviation"]
    rate = jsonObj["Cur_OfficialRate"]
    curScale = jsonObj["Cur_Scale"]
    if curScale > 1:
        return f'Курс *{abbr}* на {date} : {rate} за {curScale} {jsonObj["Cur_Name"]}'
    else : 
        return f'Курс *{abbr}* на {date} : {rate}'


def getCurrencyRate(currency_code):
    update_todays_rates()

    try:
        saved_response = rates_dict[currency_code+'_resp']
        responseContent = handleResponse(saved_response)
    except KeyError:
        update_all_rates()
        time.sleep(250)
        saved_response = rates_dict[currency_code+'_resp']
        responseContent = handleResponse(saved_response)
    finally:
        return responseContent

    
    #uri = 'https://www.nbrb.by/api/exrates/rates/'+ currency_code +'?parammode=2'
    #response = requests.get(uri)
    #if response.status_code == 200:
    #    responseContent = handleResponse(response.content)
    #    return responseContent
    #elif response.status_code == 404:
    #    return 'Not Found'

def update_todays_rates():
    now = datetime.now()
    if not 'current_date' in rates_dict or (now.date() > rates_dict['current_date'].date() and now.hour+3 >= 1 and now.hour+3 <= 23):
        rates_dict['current_date'] = now
        update_all_rates()

def convertCurrency(amount, direction):
    update_todays_rates()
    if 'usd' in direction:
        rate = getPreselectedRates('usd')
        if not rate is None:
            if direction == 'byn2usd':
                result = round(float(amount)/rate, 2);
                return f'это {result} USD'
            else:
                result = round(float(amount)*rate, 2)
                return f'это {result} BYN'
        else: 
            return 'Произошла ошибка конвертации'
    elif 'eur' in direction:
        rate = getPreselectedRates('eur')
        if not rate is None:
            if direction == 'byn2eur':
                result = round(float(amount)/rate, 2);
                return f'это {result} EUR'
            else:
                result = round(float(amount)*rate, 2)
                return f'это {result} BYN'
        else: 
            return 'Произошла ошибка конвертации'
    elif 'rub' in direction:
        rate = getPreselectedRates('rub')
        if not rate is None:
            if direction == 'byn2rub':
                result = round(float(amount)*100/rate, 1);
                return f'это {result} Российских рублей'
            else:
                result = round(float(amount)/100*rate, 2)
                return f'это {result} BYN'
        else: 
            return 'Произошла ошибка конвертации'
    else:
        return 'Not available'

