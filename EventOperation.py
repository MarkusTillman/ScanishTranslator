import logging
import sys
import UserStorage
import argparse
import Translator
import _thread
from ChatData import ChatData
import RequestHandler
import RequestSender
import Logger

eventArgumentParser = argparse.ArgumentParser()
eventArgumentParser.add_argument("--scanish", help="Scanish text to be translated to Swedish")
eventArgumentParser.add_argument("--swedish", help="Swedish text to be translated to Scanish")

def handle(request):
    Logger.logIncomingRequest(request.headers, request.get_data())
    try:
        RequestHandler.verifyRequest(request)
        jsonData = request.get_json()
        if not jsonData:
            logging.warning("Expected JSON data")
            return ""

        if "challenge" in jsonData:
            return jsonify({ "challenge" : jsonData["challenge"] })
        elif shallTranslate(jsonData):
            letNewThreadHandleTheTranslation(jsonData)
        return ""
    except:
        Logger.logUnexpectedError()
        return ""

def parseArguments(text, argumentParser):
    argumentName = text.split(" ")[0]
    argumentValue = text[len(argumentName) + 1:]
    return argumentParser.parse_args([argumentName, argumentValue])

def translateText(arguments):
    if arguments.scanish:
        return Translator.toSwedish(arguments.scanish)
    elif arguments.swedish:
        return Translator.toScanish(arguments.swedish)
    else:
        return "No text to translate"

def isCommand(text):
    return text[0] == '/'

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

def letNewThreadHandleTheTranslation(jsonData):
    _thread.start_new_thread(doTheTranslation, (jsonData, ))

def doTheTranslation(jsonData):
    try:
        translatedText = translate(jsonData)
        chatData = createChatData(jsonData, translatedText)
        RequestSender.send(chatData)
    except:
        Logger.logUnexpectedError()

def translate(jsonData):
    text = jsonData["event"]["text"]
    userId = jsonData["event"]["user"]
    arguments = parseArguments("--" + UserStorage.getTranslationModeFor(userId) + " " + text, eventArgumentParser)
    return translateText(arguments)

def createChatData(jsonData, translatedText):
    event = jsonData["event"]
    return ChatData(
        token = jsonData["token"], 
        channel = event["channel"], 
        originalText = event["text"], 
        timestamp = event["ts"], 
        userId = event["user"],
        translatedText = translatedText)