from flask import jsonify
import argparse
import RequestHandler
import UserStorage
import Logger
import Translator

argumentParser = argparse.ArgumentParser()
argumentParser.add_argument("--register", 
    help=   "Register how your text shall be translated.\n" +
            "scanish=translate from Scanish to Swedish.\n" +
            "swedish=translate from Swedish to Scanish.\n",
    metavar="languageToTranslateFrom")

def handle(request):
    Logger.logIncomingRequest(request.headers, request.get_data())
    onlyReplyToCallingUser = "ephemeral"
    try:
        RequestHandler.verifyRequest(request)
        action = parseArguments(request.form["text"], argumentParser)
        if action.register and verifyLanguageToRegister(action.register):
            UserStorage.registerUser(request.form["user_id"], action.register)
            return jsonify({"response_type": onlyReplyToCallingUser, "attachments": [{"image_url": "https://i.imgur.com/Kyd9VpM.png"}]})
        return jsonify({"response_type": onlyReplyToCallingUser, "text": argumentParser.format_help()})
    except:
        Logger.logUnexpectedError()
        return jsonify({"response_type": onlyReplyToCallingUser, "text": argumentParser.format_help()})

def parseArguments(slackText, argumentParser):
    action = slackText.split(" ")[0]
    actionArgument = slackText[len(action) + 1:]
    return argumentParser.parse_args([action, actionArgument])

def verifyLanguageToRegister(languageToTranslateFrom):
    return languageToTranslateFrom.lower() in Translator.getSupportedLanguages()