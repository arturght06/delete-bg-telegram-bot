import json
import requests
from time import sleep
import asyncio
import aiohttp
import time
import json

async def count_from_api(apikey):
    try:
        headers = {
            'accept': '*/*',
            'X-API-Key': apikey,
        }
        async with aiohttp.ClientSession() as session:
            async with session.get('https://api.remove.bg/v1.0/account', headers=headers) as response:
                return int((json.loads(await response.text()))["data"]["attributes"]["api"]["free_calls"])
    except:
        return False

    
#print(pricesString('usdt', 'uah', prices))

# {"data":{"attributes":{"credits":{"subscription":0,"payg":0,"enterprise":0,"total":0},"api":{"free_calls":-2,"sizes":"all"}}}}