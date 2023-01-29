from pymongo import MongoClient
import asyncio
import time
from time import sleep
import json

global colectiob
cluster = MongoClient('mongodb+srv://Admin:root@cluster0.wa7hj.mongodb.net/userdata?retryWrites=true&w=majority')
db = cluster['userdata']
collection = db['users']
coll_sub_list = db['sub_list']
coll_balances = db['balances']
coll_referrers = db['referrers']
coll_ref_balances = db['ref_balances']
loop = asyncio.new_event_loop()

# this function check exsistance in database
async def check(user_id):
    if collection.count_documents({'id_user': user_id}) == 1:
        cur_time = time.time()
        user_time = int(collection.find_one({'id_user': user_id})['time'])
        if user_time > cur_time:
            print(1)
            return True
        else:
            print(2)
            return False
    else:
        print(3)
        return False

# this function return dictionary of users from database
async def print_all():
    result_dict = {}
    for x in collection.find():
        # print(x)
        result_dict[x['id_user']] = x['time']
    return result_dict




# WHAT THE FUCK ARE GOING HERE...
async def get_info_db(user_id):
    if collection.count_documents({'id_user': user_id}) == 1:
        user_time = int(collection.find_one({'id_user': user_id})['time'])
        return user_time
    else:
        return False
#print(get_info('904245039'))
        
    
# this function write info in db or update it, if this is already maked
async def write(id_user, time_user):
    if collection.count_documents({'id_user': id_user}) == 1:
        collection.update_one({'id_user': id_user}, {'$set': {'time': str(time_user)}})
        return True
    elif collection.count_documents({'id_user': id_user}) == 0:
        collection.insert_one({'id_user': id_user, 'time': str(time_user)})
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


async def print_all_price():
    result_dict = {}
    for x in coll_sub_list.find():
        result_dict[x['days']] = x['price']
    return result_dict

async def write_price(days, price):
    if coll_sub_list.count_documents({'days': days}) == 1:
        coll_sub_list.update_one({'days': days}, {'$set': {'price': float(price)}})
        return True
    elif coll_sub_list.count_documents({'days': days}) == 0:
        coll_sub_list.insert_one({'days': days, 'price': float(price)})
        return True

async def delete_price(days):
    if coll_sub_list.count_documents({'days': days}) == 1:
        coll_sub_list.delete_one({'days': days})
        return True
    else:
        return False

######################################################################################################
######################################################################################################
######################################################################################################
######################################################################################################
######################################################################################################
######################################################################################################


async def print_all_balances():
    result_dict = {}
    for x in coll_balances.find():
        result_dict[x['user_id']] = x['balance']
    return result_dict

async def write_balance(user_id, balance):
    if coll_balances.count_documents({'user_id': user_id}) == 1:
        coll_balances.update_one({'user_id': user_id}, {'$set': {'balance': float(balance)}})
        return True
    elif coll_balances.count_documents({'user_id': user_id}) == 0:
        coll_balances.insert_one({'user_id': user_id, 'balance': float(balance)})
        return True

async def delete_balance(user_id):
    if coll_balances.count_documents({'user_id': user_id}) == 1:
        coll_balances.delete_one({'user_id': user_id})
        return True
    else:
        return False

async def get_user_balance(user_id):
    if coll_balances.count_documents({'user_id': user_id}) == 1:
        user_balance = round(float(coll_balances.find_one({'user_id': user_id})['balance']), 2)
        return user_balance
    else:
        return False

######################################################################################################
######################################################################################################
######################################################################################################
######################################################################################################
######################################################################################################
######################################################################################################

async def print_all_referrers():
    result_dict = {}
    for x in coll_referrers.find():
        result_dict[x['user_id']] = x['referrer']
    return result_dict

async def write_referrer(user_id, referrer):
    if coll_referrers.count_documents({'user_id': user_id}) == 1:
        coll_referrers.update_one({'user_id': user_id}, {'$set': {'referrer': int(referrer)}})
        return True
    elif coll_referrers.count_documents({'user_id': user_id}) == 0:
        coll_referrers.insert_one({'user_id': user_id, 'referrer': int(referrer)})
        return True

async def get_referrer_id(user_id):
    if coll_referrers.count_documents({'id_user': user_id}) == 1:
        referrer_id = int(coll_referrers.find_one({'id_user': user_id})['referrer'])
        return referrer_id
    else:
        return False

######################################################################################################
######################################################################################################
######################################################################################################
######################################################################################################
######################################################################################################
######################################################################################################



async def print_all_ref_balances():
    result_dict = {}
    for x in coll_ref_balances.find():
        result_dict[x['user_id']] = x['balance']
    return result_dict

async def write_ref_balance(user_id, balance):
    if coll_ref_balances.count_documents({'user_id': user_id}) == 1:
        coll_ref_balances.update_one({'user_id': user_id}, {'$set': {'balance': float(balance)}})
        return True
    elif coll_ref_balances.count_documents({'user_id': user_id}) == 0:
        coll_ref_balances.insert_one({'user_id': user_id, 'balance': float(balance)})
        return True


async def get_ref_balance(user_id):
    if coll_ref_balances.count_documents({'user_id': user_id}) == 1:
        user_balance = int(coll_ref_balances.find_one({'user_id': user_id})['balance'])
        return user_balance
    else:
        return False
