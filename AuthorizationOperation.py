import UserAccessTokenStorage
import RequestSender
import Logger
import urllib.parse

clientSecret = open("client.secret", "r").read()
clientId = "492531746400.493469272005"
permissionsForUserToAuthorize = [ "chat:write:user", "im:write" ]

def redirectToSlack(request):
    Logger.logIncomingRequest(request.headers, request.get_data())

    requestParameters = {
        "client_id":  clientId,
        "scope": str.join(' ', permissionsForUserToAuthorize)
    }
    url = "https://slack.com/oauth/authorize?" + urllib.parse.urlencode(requestParameters)
    return RequestSender.redirectRequest(request, url)

def handleCallbackFromSlack(request):
    Logger.logIncomingRequest(request.headers, request.get_data())

    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
    }
    requestParameters = {
        "client_id": clientId,
        "client_secret": clientSecret,
        "code": request.args.get("code")
    }
    url = "https://slack.com/api/oauth.access?" + urllib.parse.urlencode(requestParameters)
    response = RequestSender.post(url = url, headers = headers, username=clientId, password=clientSecret)
    persistUserAccessToken(response)
    return "Authorization successful!\n" + "Scanish translator can now translate for you! Begin by registering which language you want translated by typing \"/scanish --register swedish\" in a workspace where Scanish translator is installed!"

def persistUserAccessToken(response):
    jsonBody = response.json()
    UserAccessTokenStorage.authorizeUser(jsonBody["user_id"], jsonBody["access_token"])