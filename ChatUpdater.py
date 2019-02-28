import RequestSender
import UserAccessTokenStorage 

def updateChat(chatData):
    json = {
        "token": chatData.token,
        "channel": chatData.channel,
        "text": chatData.translatedText,
        "ts": chatData.timestamp
    }
    headers = {
        "Content-Type": "application/json;charset=utf-8",
        "Authorization": "Bearer " + UserAccessTokenStorage.getToken(chatData.userId)
    }
    url = "https://slack.com/api/chat.update"
    RequestSender.post(url = url, json = json, headers = headers)


def updateChatWithCommand(commandData):
    json = {
        "username": commandData.userName,
        "response_type": commandData.response_type,
        "text": commandData.userName + ": " + commandData.translatedText,
    }
    headers = {
        "Content-Type": "application/json;charset=utf-8"
    }
    RequestSender.post(url = commandData.response_url, json = json, headers = headers)