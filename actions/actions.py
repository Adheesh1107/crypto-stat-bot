
import logging
from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker, FormValidationAction
from rasa_sdk.events import FormValidation, SlotSet
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.forms import FormValidationAction
from rasa_sdk.types import DomainDict

from utils import services, bot_response_formatter
AVAILABLE_FIAT_PREFERENCE = ['USD','INR','EUR','GBP']
logging.basicConfig(filename='loggers/action_server.txt', filemode='a', format='%(name)s - %(levelname)s - %(message)s')
instance = services.Services()

class ActionUtterIntro(Action):

    def name(self) -> Text:
        return "action_fetch_username"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        if tracker.get_latest_input_channel() == 'slack':
            username = bot_response_formatter.fetchUsername(tracker)
            # print(username)
            return[SlotSet('username',username), SlotSet('is_username_set', True)]

        return[]
class ActionFetchCoinPrice(Action):

    def name(self) -> Text:
        return "action_fetch_coin_price"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        response = instance.fetch_price(tracker.get_slot('coin_name'),tracker.get_slot('fiat_preference'))
        print(response)

        if(tracker.get_latest_input_channel() == 'slack') :
            formated_output = bot_response_formatter.slackPriceTemplate(response, tracker.get_slot("fiat_preference"),tracker.latest_message['metadata']['out_channel'])
            # print(formated_output)
        else:
            formated_output = bot_response_formatter.defaultPriceTemplate(response,tracker.get_slot("fiat_preference"))
            dispatcher.utter_message(text=formated_output)

        # A list of coins user mentioned in the current session - can be used for comparison if needed
        all_coins_list = tracker.get_slot("all_coins_per_session") if tracker.get_slot("all_coins_per_session") != None else list()
        for coin in tracker.get_slot("coin_name"):
            if coin not in all_coins_list:
                all_coins_list.append(coin) 
        return [SlotSet('all_coins_per_session',all_coins_list), SlotSet("coin_name", None)]

class ActionCheckComparePossibility(Action):

    def name(self) -> Text:
        return "action_check_compare_possibility"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        current_coins_in_tracker = tracker.get_slot("coin_name")
        if current_coins_in_tracker != None and len(current_coins_in_tracker) >= 2:
            return[SlotSet("compare_possible", True)]

        return[SlotSet("compare_possible", None)]

class ActionCompareCoins(Action):

    def name(self) -> Text:
        return "action_compare_coins"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        response = instance.fetch_price(tracker.get_slot("coin_name"),['USD','INR'])
        # logging.warning("Inside custom action - Check compare : just printing")

        print(response)
        # dispatcher.utter_message(text="Inside compare")

        if(tracker.get_latest_input_channel() == 'slack') :
            formated_output = bot_response_formatter.slackCompareTemplate(response, ['USD','INR'],tracker.latest_message['metadata']['out_channel'])
            # print(formated_output)
        else:
            formated_output = bot_response_formatter.defaultCompareTemplate(response,['USD','INR'])
            dispatcher.utter_message(text=formated_output)

        return[SlotSet("coin_name", None), SlotSet("compare_possible", None)]














# class ActionSetCompareRequest(Action):

#     def name(self) -> Text:
#         return "action_set_compare_request"

#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

#         return[SlotSet("compare_request", True)]

# class ValidateFetchPriceForm(FormValidationAction):
#     def name(self) -> Text:
#         return "validate_fetch_price_form"
    
#     def validate_coin_name(
#             self,
#             slot_value: Any,
#             dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: DomainDict,
#         ) -> Dict[Text, Any]:
#         invalid_coins = instance.validate_coins(slot_value)
#         if invalid_coins:
#             dispatcher.utter_message(text=f"Looks like few coins were invalid. Please enter valid coins. Invalid: {','.join(invalid_coins)}")
#             return {"coin_name": None}
#         dispatcher.utter_message(text= f"You selected {slot_value} as the coins")
#         return {"coin_name" : slot_value}

#     def validate_fiat_preference(   # need to have it for list
#         self,
#         slot_value: Any,
#         dispatcher: CollectingDispatcher,
#         tracker: Tracker,
#         domain: DomainDict,
#     ) -> Dict[Text, Any]:
#         if slot_value not in AVAILABLE_FIAT_PREFERENCE:
#             dispatcher.utter_message(text=f"The fiat you mentioned is not available. Please choose among these : {'/'.join(AVAILABLE_FIAT_PREFERENCE)}")
#             return {"fiat_preference" : None}
#         dispatcher.utter_message(text= f"You selected {slot_value} as the fiat preference")
#         return {"fiat_preference" : slot_value}


# class ActionFetchCoinDetails(Action):

#     def name(self) -> Text:
#         return "action_fetch_coin_details"

#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
#         # instance = services.Services()
#         # data = instance.fetch_price(tracker.get_slot('coin_name'),tracker.get_slot('fiat_preference'))
#         # print(data)
#         print("in action - fetch details")
#         return []