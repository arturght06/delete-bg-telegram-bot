import requests, json
from time import sleep 

def bybit_otc(s1, s2):
    data = {'tokenId': s1.upper(),'currencyId': s2.upper(),'payment': '','side': '0','size': '10','page': '1','amount': '',}
    response = requests.post('https://api2.bybit.com/spot/api/otc/item/list', data=data)
    ads = json.loads(response.text)['result']['items']
    all_ads = ''
    for one_string in ads:
        oneOfAds = []
        token = one_string['tokenName']
        currency = one_string['currencyId']
        min_amount = one_string['minAmount']
        max_amount = one_string['maxAmount']
        price = float(one_string['price'])
        last_quantity = float(one_string['lastQuantity'])
        quantity = float(one_string['quantity'])
        
        printedText = f'Ціна: <b>{price}</b> | ліміти: <b>{min_amount}</b>-<b>{max_amount}</b> \nОб\'єм: <b>{last_quantity}</b>\n------------\n'
        all_ads += printedText
    return all_ads

