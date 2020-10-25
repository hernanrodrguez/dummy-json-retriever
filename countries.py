import urllib.request, urllib.parse, urllib.error
import json
import ssl
from difflib import SequenceMatcher

def Menu(data):
    print('\n\n-----------------------------------------------------')
    print('This is a country information script')
    country = input('Enter country name you want to learn, otherwise skip: ')
    if len(country) < 1:
        return -1
    country = country.lower()
    for item in data:
        if country in item['name'].lower() or country in item['nativeName'].lower():
            return item['name']
    print('\nDid you mean...')
    flag = False    
    for item in data:
        if similar(country, item['name'].lower()) > 0.8:
            print(item['name'])
            flag = True
        elif similar(country, item['nativeName'].lower()) > 0.8:
            print(item['nativeName'])
            flag = True
    if not flag:
        print('No suggestions :(')
    return 0

def ShowInfo(country, data):
    print('\nInformation from', country)
    for item in data:
        if country == item['name']:
            print('- Capital City:', item['capital'])
            print('- Alpha Code:', item['alpha3Code'])
            print('- Continent:', item['region'])
            print('- Region:', item['subregion'])
            print('- Population:', item['population'])
            print('- Native Name:', item['nativeName'])
            print('\nTo see', country, 'flag visit the link:', item['flag'])

def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()
            
# Ignore SSL certificate errors
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

url = 'https://restcountries.eu/rest/v2/all'

print('Retrieving', url)
uh = urllib.request.urlopen(url, context=ctx)
data = uh.read().decode()

try:
    js = json.loads(data)
except:
    js = None

if not js:
    print('---- Retrieve Failed ----')
    exit()

while True:
    country = Menu(js)
    if type(country) != int:
        ShowInfo(country, js)
    elif country == -1:
        exit()
        
    
