import ResponseCreator
import argparse
import UserStorage
import UserAccessTokenStorage
import Logger
import Translator

import sys

argumentParser = argparse.ArgumentParser()
argumentParser.add_argument("text", nargs='?', help="Text to translate to Scanish.")
argumentParser.add_argument("--register", action='store_true', help="Register your messages to be automatically translated.")
argumentParser.add_argument("--unregister", action='store_true', help="Unregister your messages from being automatically translated.")

def handle(request):
    onlyReplyToCallingUser = "ephemeral"
    try:
        userId = request.form["user_id"]
        arguments = argumentParser.parse_args([request.form["text"]])
        if arguments.register:
            if not UserAccessTokenStorage.hasAuthorized(userId):
                return ResponseCreator.createJsonResponse({"response_type": onlyReplyToCallingUser, "text": "You must first authorize the Scanish app at: https://impartial-ibis-5785.dataplicity.io/"})
            UserStorage.registerUser(userId)
            return ResponseCreator.createJsonResponse({"response_type": onlyReplyToCallingUser, "attachments": [{"image_url": "https://i.imgur.com/Kyd9VpM.png"}]})
        elif arguments.unregister:
            UserStorage.unregisterUser(userId)
            return ResponseCreator.createJsonResponse({"response_type": onlyReplyToCallingUser, "attachments": [{"image_url": "https://i.imgur.com/YYN18jOh.jpg"}]}) 
        elif arguments.text:
            translatedText = Translator.toScanish(arguments.text)
            return ResponseCreator.createJsonResponse({"response_type": "in_channel", "text": translatedText})
    except:
        Logger.logUnexpectedError()
        print(str(sys.exc_info()))
    return ResponseCreator.createJsonResponse({"response_type": onlyReplyToCallingUser, "text": argumentParser.format_help()})