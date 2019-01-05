import argparse
import Translator
import RequestHandler
import RequestSender
import UserStorage
import logging
from ChatData import ChatData
import sys
from flask import Flask, jsonify, request
import _thread
app = Flask(__name__)

logging.basicConfig(filename="log.log", level=logging.DEBUG, filemode="w")

commandArgumentParser = argparse.ArgumentParser()
commandArgumentParser.add_argument("--register", 
    help=   "Register how your text shall be translated.\n" +
            "\"scanish\"=translate from Scanish to Swedish.\n" +
            "\"swedish\"=translate from Swedish to Scanish.\n", 
    nargs=2,
    metavar=("scanish", "swedish"))

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
def get():
    return "I'm alive"


@app.route("/scanish", methods=["POST"])
def handleUrlEncodedCommands():
    logReceivedRequest(request)
    try:
        RequestHandler.verifyRequest(request)
        arguments = parseArguments(request.form["text"], commandArgumentParser)
        if arguments.register:
            UserStorage.registerUser(request.form["user_id"], arguments.register)
            return jsonify({
                "response_type": "ephemeral",
                "attachments": [{"image_url": "https://i.imgur.com/Kyd9VpM.png"}]
            })
        return jsonify({ "response_type": "ephemeral", "text": commandArgumentParser.format_help()})
    except:
        logging.error("Unexpected error: " + str(sys.exc_info()))
        return jsonify({ "response_type": "ephemeral", "text": commandArgumentParser.format_help()})


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
        translatedText = translatedText)