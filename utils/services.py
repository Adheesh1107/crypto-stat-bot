from typing import List
from utils import dao
from utils import cmc_data_fetcher

class Services:
    def __init__(self) -> None:
        pass

    def fetch_price(self, token:List, fiat:List):
        # need to fetch the id for all the token slugs - ping dao 
        # need to convert to multiple fiats - ping internal function (price conversion)
        token_ids = dao.fetch_token_ids(token)
        
        price_details = cmc_data_fetcher.fetch_quotes(token_ids,fiat)

        return price_details

    def compare_coins(self, token:List):
        
        token_ids = dao.fetch_token_ids(token)
        
        comparison_details = cmc_data_fetcher.fetch_quotes(token_ids)       # need to write logic

        return comparison_details

    # def validate_coins(self, token:List):

    #     result = dao.check_existance(token)
    #     if len(result) == 0:
    #         return None
    #     else:
    #         return result