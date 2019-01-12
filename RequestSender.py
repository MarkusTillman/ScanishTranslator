import requests
import Logger

import UserAccessTokenStorage

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
    headers = {
        "Content-Type": "application/json;charset=utf-8",
        "Authorization": "Bearer " + UserAccessTokenStorage.getToken(chatData.userId)
    }
    url = "https://slack.com/api/chat.update"
    Logger.logOutgoingRequest(headers, json, url)
    response = requests.post(url = url, headers = headers, json = json)
    Logger.logIncomingResponse(response.headers, response.content)