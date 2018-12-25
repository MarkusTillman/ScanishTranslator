import argparse
import Translator
import requests
from ChatData import ChatData
import sys
from flask import Flask, jsonify, request
app = Flask(__name__)

argumentParser = argparse.ArgumentParser()
argumentParser.add_argument("--scanish", help="Scanish text to be translated to Swedish")
argumentParser.add_argument("--swedish", help="Swedish text to be translated to Scanish")
accessToken = open("access.token", "r").read()

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

@app.route("/", methods=["GET"])
def get():
    return "I'm alive"


@app.route("/scanish", methods=["POST"])
def handleUrlEncodedCommands():
    try:
        arguments = parseText(request.form["text"])
        translatedText = translateText(arguments)
        return jsonify({ "response_type": "in_channel", "text": translatedText})
    except:
        return jsonify({ "response_type": "ephemeral", "text": argumentParser.format_usage()})


@app.route("/", methods=["POST"])
def handleJsonEvents():
    try:
        jsonData = request.get_json()
        print("Received: \n" + str(jsonData))
        if not jsonData:
            print("Expected JSON")
            return ""

        if "challenge" in jsonData:
            return jsonify({ "challenge" : jsonData["challenge"] })
        else:
            translateAndSend(jsonData) # todo: make asynchronously
        return ""
    except:
        print("Unexpected error:", sys.exc_info())
        return ""

def isCommand(text):
    return text[0] == '/'

def translateAndSend(jsonData):
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
    dataToUpdateChatWith = ChatData(
        token = jsonData["token"], 
        channel = event["channel"], 
        originalText = text, 
        timestamp = event["ts"], 
        translatedText = translatedText)
    json = {
        "token": dataToUpdateChatWith.token,
        "channel": dataToUpdateChatWith.channel,
        "text": dataToUpdateChatWith.originalText,
        "ts": dataToUpdateChatWith.timestamp,
        "attachments": [
            {
                "text": dataToUpdateChatWith.translatedText
            }
        ]
    }
    headers = {"Authorization": "Bearer " + accessToken}
    print("Posting: \n" + str(headers) + "\n" + str(json))
    response = requests.post("https://slack.com/api/chat.update", headers = headers, json = json)
    print("Post response: \n" + str(response.content))