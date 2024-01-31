from slack import WebClient
from slack.web.slack_response import SlackResponse
from copy import deepcopy
import os

SLACK_BOT_TOKEN = os.environ.get('SLACK_TOKEN')

UPDATE_BLOCK = [
		{
			"type": "context",
			"elements": [{
				"type": "plain_text",
				"text": "You chose :"
			}]
		},
		{
			"type": "context",
			"elements": [{
				"type": "plain_text",
				"text": "Default"
			}]
		}
	]
    
class QuickReply:
    def __init__(self) -> None:
        pass

    def updateMessage(self, payload):
        # create an instance for Slack WebClient
        slack_client = WebClient(SLACK_BOT_TOKEN)

        # take the necessary data for the slack API call from payload received
        button_clicked = payload['actions'][0]['text']['text']
        message_ts = payload['message']['ts']
        channel_id = payload['container']['channel_id']

        # Making a copy of default block
        outputBlock = deepcopy(UPDATE_BLOCK)
        outputBlock[1]["elements"][0]["text"] = button_clicked

        slack_client.chat_update(
            channel= channel_id, 
            ts=message_ts, 
            blocks=outputBlock)
        return

