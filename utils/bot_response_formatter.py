import os
from slack import WebClient
from copy import deepcopy

SLACK_BOT_TOKEN = os.environ.get('SLACK_TOKEN')
slack_client = WebClient(SLACK_BOT_TOKEN)

def fetchUsername(tracker):
    username = tracker.sender_id
    userinfo = slack_client.users_info(user=username)
    name = userinfo['user']['real_name']
    return name


DEFAULT_PRICE_HEADING = "Price of the Coin:\n"
DEFAULT_PRICE_BASIC_DETAILS = "{name}:\n\tSymbol: {symbol}\n\tCoinMarketCap Rank : {cmc_rank}\n\tCirculating Supply: {circulating_supply}\n\tMax Supply: {max_supply}\n"
DEFAULT_PRICE_FIAT_PREFERENCE = "\t{fiat_name}:\n\t\tPrice: {value}\n\t\tPercent Change in Last 24 Hours: {percent_change}\n"

def defaultPriceTemplate(api_response, fiat_preference):
    complete_details = DEFAULT_PRICE_HEADING
    for each_coin in api_response:
        name = each_coin["name"]
        symbol = each_coin["symbol"]
        circulating_supply = each_coin["circulating_supply"]
        max_supply = each_coin["max_supply"]
        cmc_rank = each_coin["cmc_rank"]
        complete_details = complete_details + DEFAULT_PRICE_BASIC_DETAILS.format(
            name=name, 
            symbol=symbol,
            circulating_supply=circulating_supply,
            max_supply=max_supply,
            cmc_rank=cmc_rank
        )
        # print(cmc_rank)
        for each_fiat_preference in fiat_preference:
            value = each_coin[each_fiat_preference]["current_price"]
            percent_change = each_coin[each_fiat_preference]["Percentage_change_in_24H"]
            
            pricing_details = DEFAULT_PRICE_FIAT_PREFERENCE.format(
                fiat_name=each_fiat_preference,
                value=value,
                percent_change=percent_change)
            complete_details = complete_details + pricing_details
    return complete_details

SLACK_PRICE_HEADING = [{
			"type": "header",
			"text": {
				"type": "plain_text",
				"text": "Market Price\t\t:\t\t "
			}
		}]
SLACK_PRICE_BASIC_DETAILS = [
        {
			"type": "section",
			"text": {
				"type": "mrkdwn",
				"text": "Symbol\t\t\t\t\t\t :    "
			}
		},
		{
			"type": "section",
			"fields": [
				{
					"type": "mrkdwn",
					"text": "CoinMarketCap Rank :\t"
				}
			]
		},
		{
			"type": "header",
			"text": {
				"type": "plain_text",
				"text": "Supply\t\n"
			}
		},
		{
			"type": "section",
			"fields": [
				{
					"type": "mrkdwn",
					"text": "- Circulating :    "
				}
			]
		},
		{
			"type": "section",
			"fields": [
				{
					"type": "mrkdwn",
					"text": "- Max            :    "
				}
			]
		},
		{
			"type": "divider"
		}]
SLACK_PRICE_FIAT_PREFERENCE = [{
			"type": "section",
			"text": {
				"type": "mrkdwn",
				"text": "*USD*"
			}
		},
		{
			"type": "section",
			"text": {
				"type": "mrkdwn",
				"text": "Price :   "
			}
		},
		{
			"type": "section",
			"text": {
				"type": "plain_text",
				"text": "Percent Change in Last 24 Hours : "
			}
		},
		{
			"type": "divider"
		}]


def slackPriceTemplate(api_response, fiat_preference, channel_id):
    
    complete_details = []
    for each_coin in api_response:
        heading = deepcopy(SLACK_PRICE_HEADING)
        basic_details = deepcopy(SLACK_PRICE_BASIC_DETAILS)
        name = each_coin["name"]
        symbol = each_coin["symbol"]
        circulating_supply = each_coin["circulating_supply"]
        max_supply = each_coin["max_supply"]
        cmc_rank = each_coin["cmc_rank"]

        heading[0]['text']['text'] = heading[0]['text']['text'] + name

        basic_details[0]['text']['text'] = basic_details[0]['text']['text'] + symbol
        basic_details[1]['fields'][0]['text'] = basic_details[1]['fields'][0]['text'] + str(cmc_rank)
        basic_details[3]['fields'][0]['text'] = basic_details[3]['fields'][0]['text'] + str(circulating_supply)
        basic_details[4]['fields'][0]['text'] = basic_details[4]['fields'][0]['text'] + str(max_supply)
        
        for each_fiat_preference in fiat_preference:
            pricing_details = deepcopy(SLACK_PRICE_FIAT_PREFERENCE)
            value = each_coin[each_fiat_preference]["current_price"]
            percent_change = each_coin[each_fiat_preference]["Percentage_change_in_24H"]
            
            pricing_details[0]['text']['text'] = "*" + each_fiat_preference + "*"
            pricing_details[1]['text']['text'] = pricing_details[1]['text']['text'] + "`" +  str(round(value,3)) + "`"
            pricing_details[2]['text']['text'] = pricing_details[2]['text']['text'] + " " +  str(round(percent_change,3))

            basic_details.extend(pricing_details)
        heading.extend(basic_details)
        complete_details.extend(heading)
    slack_client.chat_postMessage(channel=channel_id, blocks=complete_details)
    return complete_details


DEFAULT_COMPARE_HEADING = "Comparison: "
DEFAULT_COMPARE_SYMBOL_DETAILS = "Symbol : "
DEFAULT_COMPARE_PRICE_DETAILS = "Price in USD : "

def defaultCompareTemplate(api_response, fiat_preference):
	heading = DEFAULT_COMPARE_HEADING
	symbol_details = DEFAULT_COMPARE_SYMBOL_DETAILS
	price_details = DEFAULT_COMPARE_PRICE_DETAILS
	for itr in range(len(api_response)):
		name = api_response[itr]["name"]
		symbol = api_response[itr]["symbol"]
		circulating_supply = api_response[itr]["circulating_supply"]
		max_supply = api_response[itr]["max_supply"]
		cmc_rank = api_response[itr]["cmc_rank"]
		price_in_usd = api_response[itr]['USD']['current_price']

		heading = heading + name
		symbol_details = symbol_details + symbol
		price_details = price_details + str(price_in_usd)
		if itr != len(api_response)-1:
			heading = heading + " vs "
			symbol_details = symbol_details + "  |  "
			price_details = price_details + "  |  "
	return heading + "\n" + symbol_details + "\n" + price_details
		
SLACK_COMPARE_BLOCK = [
		{
			"type": "header",
			"text": {
				"type": "plain_text",
				"text": "Comparison\t\t:\t\t "
			}
		},
		{
			"type": "divider"
		},
		{
			"type": "context",
			"elements": [
				{
					"type": "mrkdwn",
					"text": "*Symbol* : "
				}
			]
		},
		{
			"type": "divider"
		},
		{
			"type": "context",
			"elements": [
				{
					"type": "mrkdwn",
					"text": "*Price in USD* : "
				}
			]
		}
	]

def slackCompareTemplate(api_response, fiat_preference, channel_id):

	complete_details = deepcopy(SLACK_COMPARE_BLOCK)
	for itr in range(len(api_response)):
		name = api_response[itr]["name"]
		symbol = api_response[itr]["symbol"]
		circulating_supply = api_response[itr]["circulating_supply"]
		max_supply = api_response[itr]["max_supply"]
		cmc_rank = api_response[itr]["cmc_rank"]
		price_in_usd = api_response[itr]['USD']['current_price']

		complete_details[0]['text']['text'] = complete_details[0]['text']['text'] + name
		complete_details[2]['elements'][0]['text'] = complete_details[2]['elements'][0]['text'] + symbol
		complete_details[4]['elements'][0]['text'] = complete_details[4]['elements'][0]['text'] + str(price_in_usd)
		if itr != len(api_response)-1:
			complete_details[0]['text']['text'] = complete_details[0]['text']['text'] + " vs "
			complete_details[2]['elements'][0]['text'] = complete_details[2]['elements'][0]['text'] + "  |  "
			complete_details[4]['elements'][0]['text'] = complete_details[4]['elements'][0]['text'] + "  |  "
	
	slack_client.chat_postMessage(channel=channel_id, blocks=complete_details)
	return complete_details