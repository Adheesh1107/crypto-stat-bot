""""
    File contains all functions used to hit API and fetch time-series data (Price of the coin, Listings, etc)
"""

from typing import List
from coinmarketcapapi import CoinMarketCapAPI
import os


COIN_MARKET_CAP_API_KEY = os.environ.get('COIN_MARKET_CAP_API_KEY')
DEFAULT_FIAT_PREFERENCE = ["USD"]

cmc = CoinMarketCapAPI(COIN_MARKET_CAP_API_KEY)

def fetch_quotes(token_id: List, fiat: DEFAULT_FIAT_PREFERENCE):
    required_api_data = ["name", "symbol", "circulating_supply", "total_supply", "max_supply","cmc_rank"]
    quotes_result = list()
    for each_id in token_id:
        temp_dict = dict()
        for each_fiat in fiat:
            api_response = cmc.cryptocurrency_quotes_latest(id=str(each_id),convert=each_fiat)
            fiat_dict = dict()
            coin_name = api_response.data[str(each_id)]["name"]
            # formating the data received from API to our requirements
            for type in required_api_data:
                if type not in temp_dict:
                    temp_dict[type] = api_response.data[str(each_id)][type]
            
            fiat_dict["current_price"] = api_response.data[str(each_id)]["quote"][each_fiat]["price"]
            fiat_dict["Percentage_change_in_24H"] = api_response.data[str(each_id)]["quote"][each_fiat]["percent_change_24h"]
            # print("Inside fetch_quotes : printing formatted values : ", temp_dict)
            temp_dict[each_fiat] = fiat_dict
        quotes_result.append(temp_dict)

    return quotes_result

# print(fetch_quotes(["1","2"], ["USD","INR"]))
