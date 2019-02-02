import _thread
import ResponseCreator
import UserStorage
import Logger
import CallbackHandler

def handle(request):
    try:
        jsonData = request.get_json()
        if "challenge" in jsonData:
            return handleChallengeRequest(jsonData["challenge"])
        elif shallTranslate(jsonData):
            _thread.start_new_thread(CallbackHandler.handleCallbackToSlack, (jsonData["token"], jsonData["event"]))
    except:
        Logger.logUnexpectedError()
    return ""

def handleChallengeRequest(challengeToken):
    return ResponseCreator.createJsonResponse({ "challenge" : challengeToken })

def shallTranslate(jsonData):
    if "event" not in jsonData:
        return False
    event = jsonData["event"]
    if "user" not in event:
        return False
    if "type" not in event: 
        return False
    if event["type"] != "message":
        return False
    if "subtype" in event:
        return False
    if isCommand(event["text"]):
        return False
    if not UserStorage.isRegisteredUser(event["user"]):
        return False
    return True
 
def isCommand(text):
    return text[0] == '/'