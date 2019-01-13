from flask import jsonify
import sys
import argparse
import RequestHandler
import UserStorage
import Logger

commandArgumentParser = argparse.ArgumentParser()
commandArgumentParser.add_argument("--register", 
    help=   "Register how your text shall be translated.\n" +
            "scanish=translate from Scanish to Swedish.\n" +
            "swedish=translate from Swedish to Scanish.\n",
    metavar="languageToTranslateFrom")

def handle(request):
    Logger.logIncomingRequest(request.headers, request.get_data())
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
        Logger.logUnexpectedError()
        return jsonify({ "response_type": "ephemeral", "text": commandArgumentParser.format_help()})

def parseArguments(text, argumentParser):
    argumentName = text.split(" ")[0]
    argumentValue = text[len(argumentName) + 1:]
    return argumentParser.parse_args([argumentName, argumentValue])