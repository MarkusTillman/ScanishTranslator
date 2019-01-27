import UserAccessTokenStorage
import RequestSender
import Logger
import urllib.parse

clientSecret = open("client.secret", "r").read()
clientId = open("client.id", "r").read()
permissionsForUserToAuthorize = [ "chat:write:user" ]

def redirectToSlack(request):
    requestParameters = {
        "client_id":  clientId,
        "scope": str.join(' ', permissionsForUserToAuthorize)
    }
    url = "https://slack.com/oauth/authorize?" + urllib.parse.urlencode(requestParameters)
    return RequestSender.redirectRequest(request, url)

def handleCallbackFromSlack(request):
    try:
        headers = {
            "Content-Type": "application/x-www-form-urlencoded",
        }
        requestParameters = {
            "client_id": clientId,
            "client_secret": clientSecret,
            "code": request.args["code"]
        }
        url = "https://slack.com/api/oauth.access?" + urllib.parse.urlencode(requestParameters)
        response = RequestSender.post(url = url, headers = headers, username=clientId, password=clientSecret)
        persistUserAccessToken(response)
        return "Authorization successful!\n" + "Scanish app can translate for you as soon as you have registered which language you want translated. Type \"/scanish --register swedish\" to tell Scanish to translate from Swedish to Scanish."
    except:
        Logger.logUnexpectedError()
        return "Unknown error"

def persistUserAccessToken(response):
    jsonBody = response.json()
    UserAccessTokenStorage.authorizeUser(jsonBody["user_id"], jsonBody["access_token"])