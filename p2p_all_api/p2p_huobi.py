import requests, json
import asyncio
import aiohttp

coin_id_list = {
    'BTC': 1,
    'USDT': 2,
    'ETH': 3,
    'HT': 4,
    'EOS': 5,
    'HUSD': 6,
    'XRP': 7,
    'LTC': 8,
    }
currency_list = {
    'USD': 2,
    'HKD': 13,
    'VND': 5,
    'MYR': 22,
    'TWD': 10,
    'MAD': 41,
    'MXN': 42,
    'RUB': 11,
    'AUD': 7,
    'SGD': 3,
    'GBP': 12,
    'EUR': 14,
    'PHP': 17,
    'INR': 4,
    'CHF': 9,
    'NGN': 15,
    'IDR': 16,
    'KHR': 18,
    'BRL': 19,
    'SAR': 20,
    'AED': 21,
    'TRY': 23,
    'NZD': 24,
    'ZAR': 26,
    'NOK': 27,
    'DKK': 28,
    'SEK': 29,
    'ARS': 30,
    'THB': 31,
    'COP': 32,
    'VES': 33,
    'KES': 34,
    'PEN': 35,
    'CZK': 37,
    'HUF': 38,
    'PLN': 43,
    'RON': 44,
    'UAH': 45,
    'CLP': 53,
    'GEL': 56,
    'KZT': 57,
    'QAR': 59,
    'UYU': 60,
    'PKR': 62,
    'BBD': 66,
    'BOB': 70,
    'EGP': 74,
    'GHS': 75,
    'LKR': 83,
    'PAB': 88,
    'PYG': 90,
    'UGX': 95,
    }

pay_types_list = {
    'wise': 34,
    'monobank': 49,
    'privatbank': 33,
    'pumb': 37,
    'banktransfer': 1,
    'a-bank': 149,
    'oschadbank': 350,
    'raiffeisenbankaval': 155,
    'sportbank': 156,
    'girocard': 209,
    'paysera': 112,
    'settlepay': 116,
    'oxxo': 398,
    'izibank': 499,
    'zen': 527,
    'santanderpoland': 565,
    'raiffeisenbank': 36,
    'ukrsibbank': 154,
    'otpbank': 45,
    'kredobank': 153,
    'ideabank': 151,
    'tascombank': 157,
    'forwardbank': 148,
    'creditagricole': 414,
    'advcash': 20,
    'sberbank': 29,
    'bankpivdenny': 150,
    'geopay': 164,
    'neo': 306,
    'qiwi': 9,
    'revolut': 41,
    'tinkoff': 28,
    'cashdeposit': 21,
    'payall': 406,
    'applepay': 77,
    'easypay': 56,
    'yandexmoney': 19,
    'skrill': 40,
    '1+winner': 64,
    'googlepay': 86,
    'zelle': 392,
    'airtm': 75,
    'bancopichincha': 372,
    'perfectmoney': 43,
    'neteller': 13,
    'payeer': 24,
    'westernunion': 5,
    'paysend': 407,
    'alipay': 2,
    'wechat': 3,
    'swift': 6,
    'paytm': 8,
    }

async def p2p_huobi(s1, s2, buy_sell, *arr):
    if len(arr) == 0:
        payTypes = ''
        transAmount = None
    elif len(arr) == 1:
        if str(arr[0]).isdigit():
            transAmount = arr[0]
            payTypes = ''
        else:
            payTypes = arr[0]
            transAmount = None
    elif len(arr) == 2:
        if str(arr[0]).isdigit():
            transAmount = arr[0]
            payTypes = arr[1]
        else:
            transAmount = arr[1]
            payTypes = arr[0]

    s1 = s1.upper()
    s2 = s2.upper()
    if s1 not in coin_id_list or s2 not in currency_list:
        return False
    else:
        s1 = str(coin_id_list[s1])
        s2 = str(currency_list[s2])

    if buy_sell.upper() == 'BUY':
        buy_sell = 'sell'
    elif buy_sell.upper() == 'SELL':
        buy_sell = 'buy'
    else:
        return False

    if payTypes != '':
        try:
            payTypes = pay_types_list[payTypes.lower().replace(' ', '')]
        except:
            return False
    
    headers = {
        'authority': 'otc-api.trygofast.com',
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'ru,en-UA;q=0.9,en;q=0.8,ru-UA;q=0.7,en-US;q=0.6,uk;q=0.5,pl;q=0.4',
        'client-type': 'web',
        'origin': 'https://c2c.huobi.com',
        'otc-language': 'ru-RU',
        'portal': 'web',
        'referer': 'https://c2c.huobi.com/',
        'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="102", "Google Chrome";v="102"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'cross-site',
        'token': 'undefined',
        'trace_id': '8faa3097-04b6-4795-b628-c9b5f91c806e',
        'uid': '0',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36',
        'x-requested-with': 'XMLHttpRequest',
    }
    
    params = {
        'coinId': s1,
        'currency': s2,
        'tradeType': buy_sell,
        'currPage': '1',
        'payMethod': str(payTypes),
        'acceptOrder': '0',
        'country': '',
        'blockType': 'general',
        'online': '1',
        'range': '0',
        'amount': '',
        'isThumbsUp': 'false',
        'isMerchant': 'false',
        'isTraded': 'false',
        'onlyTradable': 'false',
    }
    if transAmount != None:
        params['amount'] = transAmount

    async with aiohttp.ClientSession(headers=headers) as session:
        async with session.get(f'https://otc-api.mycdncache.com/v1/data/trade-market', params=params) as resp:
            content = await resp.content.read()


            json_req = json.loads(content)
            #pprint(json_req['data'])
            try:
                data = json_req['data']
                result_all = []
                for i in range(len(data)):
                    price = data[i]['price']
                    amount = data[i]['tradeCount']
                    minAmount = data[i]['minTradeLimit']
                    maxAmount = data[i]['maxTradeLimit']

                    tradeMethods = data[i]['payMethods']
                    methods = ''
                    for t in range(0, len(tradeMethods)):
                        trade_method = tradeMethods[t]['name']
                          
                        if t == len(tradeMethods)-1:
                            methods += trade_method
                        else:
                            methods += trade_method + ', '
                    
                    result_one = [price, amount, minAmount, maxAmount, methods]
                    result_all.append(result_one)
                if len(result_all) == 0:
                    await session.close()
                    return False
                else:
                    await session.close()
                    return result_all
            except:
                await session.close()
                return False
        


# resp = p2p_huobi('usDt', 'Uah', 'Buy', '1000', 'monobank')
# if resp == False:
#     print('False')
# else:
#     print(resp[0])
