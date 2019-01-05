import argparse
import Translator
import RequestHandler
import RequestSender
import logging
from ChatData import ChatData
import sys
from flask import Flask, jsonify, request
app = Flask(__name__)

logging.basicConfig(filename="log.log", level=logging.DEBUG, filemode="w")
argumentParser = argparse.ArgumentParser()
argumentParser.add_argument("--scanish", help="Scanish text to be translated to Swedish")
argumentParser.add_argument("--swedish", help="Swedish text to be translated to Scanish")

def parseText(text):
    command = text.split(" ")[0]
    textToTranslate = text[len(command) + 1:]
    return argumentParser.parse_args([command, textToTranslate])

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
    RequestHandler.verifyRequest(request)
    try:
        arguments = parseText(request.form["text"])
        translatedText = translateText(arguments)
        return jsonify({ "response_type": "in_channel", "text": translatedText})
    except:
        return jsonify({ "response_type": "ephemeral", "text": argumentParser.format_usage()})


@app.route("/", methods=["POST"])
def handleJsonEvents():
    logReceivedRequest(request)
    RequestHandler.verifyRequest(request)
    try:
        jsonData = request.get_json()
        if not jsonData:
            logging.warning("Expected JSON data")
            return ""

        if "challenge" in jsonData:
            return jsonify({ "challenge" : jsonData["challenge"] })
        else:
            # todo: make asynchronously
            chatData = translate(jsonData)
            RequestSender.send(chatData)
        return ""
    except:
        logging.error("Unexpected error: " + sys.exc_info())
        return ""

def isCommand(text):
    return text[0] == '/'

def translate(jsonData):
    # todo: verify jsonData (body)
    if "event" not in jsonData:
        return
    event = jsonData["event"]
    if "type" not in event: 
        return
    if event["type"] != "message":
        return 
    if "subtype" in event:
        return
    text = event["text"]
    if (isCommand(text)):
        return

    arguments = parseText("--scanish " + text) # todo: make configuration using new command.
    translatedText = translateText(arguments)
    return ChatData(
        token = jsonData["token"], 
        channel = event["channel"], 
        originalText = text, 
        timestamp = event["ts"], 
        translatedText = translatedText)