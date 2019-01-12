import logging
import base64
import requests
import UserAccessTokenStorage
from flask import redirect
from http import HTTPStatus
import Logger

clientSecret = open("client.secret", "r").read()
clientId = "492531746400.493469272005" # todo: file
permissionsToAuthorize = [ "chat:write:user", "im:write" ] # todo: file

def redirectToSlack(request):
    Logger.logIncomingRequest(request.headers, request.get_data())

    requestParameters = {
        "client_id":  clientId,
        "scope": str.join(' ', permissionsToAuthorize)
    }
    formattedRequestParameters = '&'.join("{!s}={!s}".format(key, value) for (key, value) in requestParameters.items())
    url = "https://slack.com/oauth/authorize?" + formattedRequestParameters
    logging.info("Redirecting GET request to " + url)
    response = redirect(url, HTTPStatus.FOUND)
    return response

def handleCallbackFromSlack(request):
    Logger.logIncomingRequest(request.headers, request.get_data())

    verificationCode = request.args.get("code")
    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "Authorization": "Basic " + base64.b64encode((clientId + ":" + clientSecret).encode("UTF-8")).decode("UTF-8")
    }
    requestParameters = {
        "client_id": clientId,
        "client_secret": clientSecret,
        "code": verificationCode
    }
    formattedRequestParameters = '&'.join("{!s}={!s}".format(key, value) for (key, value) in requestParameters.items())
    url = "https://slack.com/api/oauth.access?" + formattedRequestParameters
    Logger.logOutgoingRequest(headers, requestParameters, url)
    response = requests.post(url = url, headers = headers)
    Logger.logIncomingResponse(response.headers, response.content)
   
    jsonBody = response.json()
    UserAccessTokenStorage.authorizeUser(jsonBody["user_id"], jsonBody["access_token"])
    return "Authorization successful!\n" + "Scanish translator can now translate for you! Begin by registering which language you want translated by typing \"/scanish --register swedish\" in a workspace where Scanish translator is installed!"