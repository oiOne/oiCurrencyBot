import requests
from bs4 import BeautifulSoup
from datetime import datetime, date

realt_dict = {}

def getParsedData():
    BASE_URL = 'https://realt.by/gomel-region/statistics/'
    r = requests.get(BASE_URL)
    soap = BeautifulSoup(r.text, "html.parser")
    cost_info = soap.select('div.col-xs-12.col-md-6')
    return cost_info[0].text

def update_todays_flag():
    now = datetime.now()
    if not 'current' in realt_dict or now.date() > realt_dict['current'].date():
        realt_dict['current'] = now
        r = getParsedData()
        realt_dict['costm2'] = r

def getRealtByCost():
    update_todays_flag()
    if not 'costm2' in realt_dict:
        now = datetime.now()
        realt_dict['current'] = now
        r = getParsedData()
        realt_dict['costm2'] = r
    
    return realt_dict['costm2'];