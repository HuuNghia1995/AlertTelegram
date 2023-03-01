import requests
import datetime
import configparser
import ChatBotTelegram
import ast
import time
from requests.auth import HTTPBasicAuth
import json

config = configparser.ConfigParser()
config.read("config.conf")
ES_HOST = config.get("SERVER_ES", "server")
ES_PORT = config.get("SERVER_ES", "port")
username_ = config.get("SERVER_ES", "username_")
password_ = config.get("SERVER_ES", "password_")
duration = int(config.get("SERVER_ES", "duration"))
index_string = config.get("SERVER_ES", "index")
index_list = index_string.split(',')
start_time = (datetime.datetime.utcnow() - datetime.timedelta(minutes=duration)).strftime("%Y-%m-%dT%H:%M:%S.%fZ")
end_time = datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S.%fZ")
count = 0

if __name__ == "__main__":
    for index in index_list:
        url_count = f"{ES_HOST}:{ES_PORT}/{index}/_count"
        url_list = f"{ES_HOST}:{ES_PORT}/{index}/_search"

        # Query
        headers = {
            "Content-Type": "application/json"
        }
        query = {
            "size":10000,
            "query": {
                "bool": {
                    "must": [
                        # *[{"match": {field: value}} for field, value in filters.items()],
                        {"range": {"@timestamp": {"gte": start_time, "lt": end_time}}}
                    ]
                }
            }
        }

        matching_sections = []
        for section in config.sections():
            if config.get(section, 'index') == index:
                matching_sections.append(section)
        response_list = requests.get(url_list, auth=HTTPBasicAuth(username_, password_), headers=headers, json=query)
        if response_list.status_code != 200:
            break
        data = json.loads(response_list.content)
        for section in matching_sections:
            if section == 'SERVER_ES': continue
            filters = ast.literal_eval(config.get(section, "filters"))
            threshold = int(config.get(section, "threshold"))
            bot_token = config.get(section, "bot_token")
            chat_group_id = config.get(section, "chat_group_id")
            message_ = config.get(section, "message_")

            filtered_data = data['hits']['hits']
            for field_name, field_value in filters.items():
                # if isinstance(field_value, list):
                filtered_data = [item for item in filtered_data if item['_source'][field_name] in field_value]
            count = len(filtered_data)
            if count > threshold:
                ChatBotTelegram.send_message_to_telegram(bot_token,chat_group_id,message_)
            else:
                break
            time.sleep(2)
