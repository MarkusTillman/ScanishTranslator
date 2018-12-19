import argparse
import Translator
import requests
from flask import Flask, jsonify, request
app = Flask(__name__)

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

def errorResponse(usage):
    return jsonify(
        response_type = "ephemeral",
        text = usage
    )

def response(translatedText):
    return jsonify(
        response_type = "in_channel",
        text = translatedText
    )

@app.route("/scanish", methods=["POST"])
def home():
    try:
        arguments = parseText(request.form["text"])
        translatedText = translateText(arguments)
        requests.post("https://hooks.slack.com/services/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", json={"text":"testing webhook"})
        return response(translatedText)
    except:
        return errorResponse(argumentParser.format_usage())