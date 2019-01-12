import argparse
import Translator
import RequestHandler
import RequestSender
import UserStorage
import AuthorizationOperation
import CommandOperation
import logging
from ChatData import ChatData
import sys
from flask import Flask, request
import _thread

app = Flask(__name__)
logging.basicConfig(filename="log.log", level=logging.DEBUG, filemode="w")

eventArgumentParser = argparse.ArgumentParser()
eventArgumentParser.add_argument("--scanish", help="Scanish text to be translated to Swedish")
eventArgumentParser.add_argument("--swedish", help="Swedish text to be translated to Scanish")

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

def logReceivedRequest(request):
    logging.info("Received: " + str(request.headers) + str(request.get_data()))

@app.route("/", methods=["GET"])
def handleUserAuthorizationOfApp():
    logReceivedRequest(request)
    return AuthorizationOperation.handleRedirect(request)

@app.route("/verificationCode", methods=["GET"])
def handleAuthorizationCallback():
    logReceivedRequest(request)
    return AuthorizationOperation.handleCallback(request)

@app.route("/scanish", methods=["POST"])
def handleSlackCommand():
    logReceivedRequest(request)
    return CommandOperation.handle(request)

@app.route("/", methods=["POST"])
def handleJsonEvents():
    logReceivedRequest(request)
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
        logging.error("Unexpected error: " + str(sys.exc_info()))
        return ""

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
        logging.error("Unexpected error: " + str(sys.exc_info()))

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