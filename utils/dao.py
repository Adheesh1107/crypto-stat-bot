from typing import List
from pymongo import MongoClient, collection
import os
# import pandas as pd

# environment variables
MONGO_DB_URL = os.environ.get('MONGO_DB_URL')
COIN_MARKET_CAP_API_KEY = os.environ.get('COIN_MARKET_CAP_API_KEY')

# Database connections
client = MongoClient(MONGO_DB_URL)
dbname = client['crypto_stat_bot']
cmc_cryptocurrency_map = dbname['cmc_cryptocurrency_map']

def fetch_token_ids(token:List):
    token_id = list()
    for word in token:
        # for query_result in cmc_cryptocurrency_map.find({"slug":slug}):
        #     print(query_result['id'])

        # finding the correct coin details
        # print(pd.DataFrame(cmc_cryptocurrency_map.find({ '$or' : [ {"slug":word}, {"symbol":word}, {"name":word} ] })))
        token_id.append(cmc_cryptocurrency_map.find({
            '$or' : [ 
                {"slug":word},
                {"symbol":word},
                {"name":word}
            ]
        })[0]['id'])
    return token_id

def check_existance(token:List):
    invalid_coins = list()
    for word in token:
        if not len(list(cmc_cryptocurrency_map.find({
            '$or' : [ 
                {"slug":word},
                {"symbol":word},
                {"name":word}
            ]
        }))):
            invalid_coins.append(word)
    return invalid_coins

# print(fetch_token_ids(["ETH", "bitcoin","xrp"]))
