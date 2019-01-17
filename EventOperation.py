import _thread
from flask import jsonify

import UserStorage
import Logger
import EventTranslator

def handle(request):
    try:
        jsonData = request.get_json()
        if "challenge" in jsonData:
            return handleChallengeRequest(jsonData)
        elif shallTranslate(jsonData):
            _thread.start_new_thread(EventTranslator.handleCallbackToSlack, (jsonData["token"], jsonData["event"]))
    except:
        Logger.logUnexpectedError()
    return ""

def handleChallengeRequest(jsonData):
    return jsonify({ "challenge" : jsonData["challenge"] })

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