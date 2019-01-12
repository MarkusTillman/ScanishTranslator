import logging
import base64
import requests
import UserAccessTokenStorage
from flask import redirect
from http import HTTPStatus

clientSecret = open("client.secret", "r").read()
clientId = "492531746400.493469272005" # todo: file
permissionsToAuthorize = [ "chat:write:user", "im:write" ] # todo: file

def handleRedirect(request):
    requestParameters = {
        "client_id":  clientId,
        "scope": str.join(' ', permissionsToAuthorize)
    }
    formattedRequestParameters = '&'.join("{!s}={!s}".format(key, value) for (key, value) in requestParameters.items())
    url = "https://slack.com/oauth/authorize?" + formattedRequestParameters
    logging.info("Redirecting GET request to " + url)
    response = redirect(url, HTTPStatus.FOUND)
    return response

def handleCallback(request):
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
    logging.info("Posting request: \n" + str(headers) + "\n" + str(requestParameters))
    response = requests.post("https://slack.com/api/oauth.access", headers = headers, data = requestParameters)
    logging.info("Post response: \n" + str(response.content))
   
    jsonBody = response.json()
    UserAccessTokenStorage.authorizeUser(jsonBody["user_id"], jsonBody["access_token"])
    return "Authorization successful!"