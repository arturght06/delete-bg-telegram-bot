import requests, json
from pprint import pprint
import asyncio
import aiohttp
from fees.deposit.huobi import fee_deposit as dep_hb
from fees.withdraw.huobi import fee_withdraw as with_hb
from fees.deposit.binance import fee_deposit as dep_bin
from fees.withdraw.binance import fee_withdraw as with_bin

from fees.withdraw.exmo import fee_withdraw as with_exmo
import time

try:
    loop = asyncio.get_event_loop()
except:
    loop = asyncio.get_event_loop()

# inp = input('token---')

start = time.time()

a = loop.run_until_complete(with_exmo('eur'))
# b = loop.run_until_complete(with_hb(inp))

print('spot_time:',start - time.time())
# print('deposit')
pprint(a)

