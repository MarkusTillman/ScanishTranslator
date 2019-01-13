import requests
from flask import redirect
from http import HTTPStatus
import logging
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

def redirectRequest(request, url):
    logging.info("Redirecting request to " + url)
    return redirect(url, HTTPStatus.FOUND)

def post(url, data=None, json=None, username=None, password=None, **kwargs):
    headers = kwargs.get("headers")
    body = json if data is None else data
    authorization = requests.auth.HTTPBasicAuth(username, password)
    Logger.logOutgoingRequest(headers, body, url)
    response = requests.post(url = url, data = data, json = json, auth = authorization, **kwargs)
    Logger.logIncomingResponse(response.headers, response.content)
    return response