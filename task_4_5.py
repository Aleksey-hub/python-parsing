'''
4) Написать запрос к базе, который вернет список подписчиков только указанного пользователя
5) Написать запрос к базе, который вернет список профилей, на кого подписан указанный пользователь
'''
from pprint import pprint

from pymongo import MongoClient

client = MongoClient('127.0.0.1', 27017)
mongo_db = client['instagram']

collection = mongo_db['instagram']

# список подписчиков пользователя teh_remo_61
for follower in collection.find({'user_name': 'teh_remo_61', 'is_follower': True}):
    pprint(follower)

# список профилей, на кого подписан teh_remo_61
for following in collection.find({'user_name': 'teh_remo_61', 'is_following': True}):
    pprint(following)

