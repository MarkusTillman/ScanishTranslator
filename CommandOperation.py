import ResponseCreator
import argparse
import UserStorage
import UserAccessTokenStorage
import Logger
import Translator

argumentParser = argparse.ArgumentParser()
argumentParser.add_argument("--register", 
    help=   "Register how your text shall be translated.\n" +
            "scanish=translate from Scanish to Swedish.\n" +
            "swedish=translate from Swedish to Scanish.\n",
    metavar="languageToTranslateFrom")

def handle(request):
    onlyReplyToCallingUser = "ephemeral"
    try:
        userId = request.form["user_id"]
        if not UserAccessTokenStorage.hasAuthorized(userId):
            return ResponseCreator.createJsonResponse({"response_type": onlyReplyToCallingUser, "text": "You must first authorize the Scanish app at: https://impartial-ibis-5785.dataplicity.io/"})
        action = parseArguments(request.form["text"])
        if action.register and verifyLanguageToRegister(action.register):
            UserStorage.registerUser(userId, action.register)
            return ResponseCreator.createJsonResponse({"response_type": onlyReplyToCallingUser, "attachments": [{"image_url": "https://i.imgur.com/Kyd9VpM.png"}]})
    except:
        Logger.logUnexpectedError()
    return ResponseCreator.createJsonResponse({"response_type": onlyReplyToCallingUser, "text": argumentParser.format_help()})

def parseArguments(slackText):
    action = slackText.split(" ")[0]
    actionArgument = slackText[len(action) + 1:]
    return argumentParser.parse_args([action, actionArgument])

def verifyLanguageToRegister(languageToTranslateFrom):
    return languageToTranslateFrom.lower() in Translator.getSupportedLanguages()