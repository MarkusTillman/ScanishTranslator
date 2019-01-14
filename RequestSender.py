import requests
from flask import redirect
from http import HTTPStatus
import logging
import Logger

def redirectRequest(request, url):
    logging.info("Redirecting request to " + url)
    return redirect(url, HTTPStatus.FOUND)

def post(url, data=None, json=None, username=None, password=None, **kwargs):
    headers = kwargs.get("headers")
    body = json if data is None else data
    basicAuthorization = None
    if username != None and password != None:
        basicAuthorization = requests.auth.HTTPBasicAuth(username, password)
    Logger.logOutgoingRequest(headers, body, url)
    response = requests.post(url = url, data = data, json = json, auth = basicAuthorization, **kwargs)
    Logger.logIncomingResponse(response.headers, response.content)
    return response