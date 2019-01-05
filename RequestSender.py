import logging
import requests

accessToken = open("access.token", "r").read()

def send(chatData):
    json = {
        "token": chatData.token,
        "channel": chatData.channel,
        "text": chatData.originalText,
        "ts": chatData.timestamp,
        "attachments": [
            {
                "text": chatData.translatedText
            }
        ]
    }
    headers = {"Authorization": "Bearer " + accessToken}
    logging.info("Posting request: \n" + str(headers) + "\n" + str(json))
    response = requests.post("https://slack.com/api/chat.update", headers = headers, json = json)
    logging.info("Post response: \n" + str(response.content))