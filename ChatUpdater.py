import RequestSender
import UserAccessTokenStorage 

def updateChat(chatData):
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
    RequestSender.post(url = url, json = json, headers = headers)