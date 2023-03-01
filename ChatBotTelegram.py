import requests
import time
from requests.auth import HTTPBasicAuth
import json

def send_message_to_telegram(bot_token,chat_group_id,message_):
    stop_alert = " "
    end_time_alert = time.time() + 15
    count_message = 0

    while count_message < 11 and time.time() < end_time_alert :
        # Check if the maximum duration has been reached
        time.sleep(3)
        #stop_alert = get_last_message_text(bot_token)
        #print(make_request(bot_token, chat_group_id, message_), stop_alert)
        # if stop_alert == "/stop":
        #     break
        if make_request(bot_token, chat_group_id, message_) is not None:
            count_message +=1

#fielter
def get_last_message_text(bot_token):
    # Replace the placeholder with your own Telegram Bot API information
    # Get updates from the Telegram group
    time.sleep(60)
    response = requests.get(f"https://api.telegram.org/bot{bot_token}/getUpdates")
    if response.status_code == 200:
        data = json.loads(response.content)
        #if data['result']:
        last_update = data['result'][-1]
        return last_update['message']['text']


def make_request(bot_token, chat_group_id, message_):
    try:
        response = requests.get(f"https://api.telegram.org/bot{bot_token}/sendMessage?chat_id={chat_group_id}&text={message_}")
        response.raise_for_status() # raise an exception if status code is not 200
        return response.json()
    except requests.exceptions.RequestException as e:
        #print(f"Error: {e}")
        return None