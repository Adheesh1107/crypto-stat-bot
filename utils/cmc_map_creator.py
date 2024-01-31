"""
    This program is used to fetch the latest CoinMarketCap's cryptocurrency map and store it to a MongoDB
    Database name - crypto_stat_bot
    Collection name - cmc_cryptocurrency_map
"""

from coinmarketcapapi import CoinMarketCapAPI
import os
from pymongo import MongoClient

# Get environment variables
MONGO_DB_URL = os.environ.get('MONGO_DB_URL')
COIN_MARKET_CAP_API_KEY = os.environ.get('COIN_MARKET_CAP_API_KEY')

# fetching the map
cmc = CoinMarketCapAPI(COIN_MARKET_CAP_API_KEY)
result = cmc.cryptocurrency_map()
# print(result.credit_count)

# Database connections
client = MongoClient(MONGO_DB_URL)
dbname = client['crypto_stat_bot']
collection_name = dbname['cmc_cryptocurrency_map']

""" Loops through all the coin data and stores it to the collection named - "cmc_cryptocurrency_map"""
for item in result.data:
    insert_data = {
        "id": item["id"],
        "slug": item["slug"],
        "name": item["name"],
        "symbol": item["symbol"],
        "first_historical_data": item["first_historical_data"],
        "rank": item["rank"]
    }
    print(insert_data)
    collection_name.insert_one(insert_data)
