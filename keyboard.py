# Keyboards for bot
from telebot import types

def getRatesKeyboard():
    ratesKB = types.InlineKeyboardMarkup()
    
    key_usd = types.InlineKeyboardButton(text='USD', callback_data='usd')
    ratesKB.add(key_usd)
    
    key_eur = types.InlineKeyboardButton(text='EUR', callback_data='eur')
    ratesKB.add(key_eur)
    
    key_rub = types.InlineKeyboardButton(text='RUB', callback_data='rub')
    ratesKB.add(key_rub)
    
    return ratesKB;

def getMainKeyboard():
    mainKB = types.InlineKeyboardMarkup()
    
    key_rates = types.InlineKeyboardButton(text='Курсы', callback_data='rates')
    mainKB.add(key_rates)
    
    key_converter = types.InlineKeyboardButton(text='Конвертер', callback_data='converter')
    mainKB.add(key_converter)
    
    key_costm2 = types.InlineKeyboardButton(text='Цена кв. метра', callback_data='costm2')
    mainKB.add(key_costm2)
    
    return mainKB;

def getConverterKeyboard():
    ratesKB = types.InlineKeyboardMarkup(row_width=2)
    key_byn2usd = types.InlineKeyboardButton(text='BYN -> USD', callback_data='byn2usd')
    key_usd2byn = types.InlineKeyboardButton(text='USD -> BYN', callback_data='usd2byn')
    ratesKB.add(key_byn2usd, key_usd2byn)

    key_byn2eur = types.InlineKeyboardButton(text='BYN -> EUR', callback_data='byn2eur')
    key_eur2byn = types.InlineKeyboardButton(text='EUR -> BYN', callback_data='eur2byn')
    ratesKB.add(key_byn2eur, key_eur2byn)

    key_byn2rub = types.InlineKeyboardButton(text='BYN -> RUB', callback_data='byn2rub')
    key_rub2byn = types.InlineKeyboardButton(text='RUB -> BYN', callback_data='rub2byn')
    ratesKB.add(key_byn2rub, key_rub2byn)

    return ratesKB;

 




