import logging
import sys
import UserStorage
import argparse
import Translator
import _thread
from ChatData import ChatData
import RequestSender
import Logger
from flask import jsonify

argumentParser = argparse.ArgumentParser()
argumentParser.add_argument("--scanish", help="Translate Scanish to Swedish")
argumentParser.add_argument("--swedish", help="Translate Swedish to Scanish")

def handle(request):
    try:
        jsonData = request.get_json()
        if "challenge" in jsonData:
            return handleChallengeRequest(jsonData)
        elif shallTranslate(jsonData):
            letNewThreadHandleTheTranslation(jsonData)
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

def letNewThreadHandleTheTranslation(jsonData):
    _thread.start_new_thread(handleTheTranslation, (jsonData, ))

def handleTheTranslation(jsonData):
    try:
        originalText = jsonData["event"]["text"]
        userId = jsonData["event"]["user"]
        translatedText = translateTextForUser(originalText, userId)
        if originalText != translatedText:
            chatData = createChatData(jsonData, translatedText)
            RequestSender.send(chatData)
        else:
            logging.info("Did not send request to translate: text is same after translation")
    except:
        Logger.logUnexpectedError()

def translateTextForUser(textToTranslate, userId):
    languageToTranslate = UserStorage.getTranslationModeFor(userId)
    action = argumentParser.parse_args(["--" + languageToTranslate, textToTranslate])
    if action.scanish:
        return Translator.toSwedish(action.scanish)
    elif action.swedish:
        return Translator.toScanish(action.swedish)
    else:
        return "No text to translate"

def createChatData(jsonData, translatedText):
    event = jsonData["event"]
    return ChatData(
        token = jsonData["token"], 
        channel = event["channel"], 
        originalText = event["text"], 
        timestamp = event["ts"], 
        userId = event["user"],
        translatedText = translatedText)