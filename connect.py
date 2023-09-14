from pymongo import MongoClient
import asyncio
import time
from time import sleep
import json
from config import mongodb_cluster_link
import aiohttp


global colectiob
cluster = MongoClient(mongodb_cluster_link)
db = cluster['removebg']
collection = db['users']
coll_keys = db['apikeys']
loop = asyncio.new_event_loop()

# this function check exsistance in database
async def check(user_id):
    if collection.count_documents({'id_user': user_id}) == 1:
        user_count = int(collection.find_one({'id_user': user_id})['count'])
        if user_count > 0:
            # print(1)
            return True
        else:
            # print(2)
            return False
    else:
        # print(3)
        return False

# this function return dictionary of users from database
async def print_all():
    result_dict = {}
    for x in collection.find():
        # print(x)
        result_dict[x['id_user']] = x['count']
    return result_dict


async def check_exist(user_id):
    if collection.count_documents({'id_user': user_id}) == 1:
        return True
    elif collection.count_documents({'id_user': user_id}) == 0:
        collection.insert_one({'id_user': str(user_id), 'count': 40})
        return True

# WHAT THE FUCK ARE GOING HERE...
async def get_info_db(user_id):
    if collection.count_documents({'id_user': user_id}) == 1:
        user_time = int(collection.find_one({'id_user': user_id})['count'])
        return user_time
    else:
        return False
#print(get_info('904245039'))
        
    
# this function write info in db or update it, if this is already maked
async def write(id_user, count):
    if collection.count_documents({'id_user': id_user}) == 1:
        collection.update_one({'id_user': str(id_user)}, {'$set': {'count': int(count)}})
        return True
    elif collection.count_documents({'id_user': id_user}) == 0:
        collection.insert_one({'id_user': str(id_user), 'count': 3})
        return True
    else:
        return False

# this function delete user from database
async def delete(user_id):
    if collection.count_documents({'id_user': user_id}) == 1:
        collection.delete_one({'id_user': user_id})
        return True
    else:
        return False


######################################################################################################
######################################################################################################
######################################################################################################
######################################################################################################
######################################################################################################
######################################################################################################

async def get_real_count(api_key):
    async with aiohttp.ClientSession() as session:
        headers = {'X-Api-Key': api_key}
        async with session.get('https://api.remove.bg/v1.0/account', headers=headers) as response:
            result_json = json.loads(await response.read())
            free_keys = int(result_json['data']['attributes']['api']['free_calls'])
            return free_keys


async def print_all_keys():
    result_dict = {}
    for x in coll_keys.find():
        result_dict[x['key']] = int(x['count'])
    return result_dict

async def write_key(key):
    count = int(await get_real_count(key))
    if coll_keys.count_documents({'key': key}) == 1:
        coll_keys.update_one({'key': key}, {'$set': {'count': count}})
        return True
    elif coll_keys.count_documents({'key': key}) == 0:
        coll_keys.insert_one({'key': key, 'count': count})
        return True

async def delete_key(key):
    if coll_keys.count_documents({'key': str(key)}) == 1:
        coll_keys.delete_one({'key': str(key)})
        return True
    else:
        return False

async def get_count(key):
    if coll_keys.count_documents({'key': key}) == 1:
        count = int(coll_keys.find_one({'key': key})['count'])
        return count
    else:
        return False
