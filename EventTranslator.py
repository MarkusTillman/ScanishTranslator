import logging
import argparse

import ChatUpdater
from ChatData import ChatData
import Translator
import UserStorage
import Logger

translationParser = argparse.ArgumentParser()
translationParser.add_argument("--scanish", help="Translate Scanish to Swedish")
translationParser.add_argument("--swedish", help="Translate Swedish to Scanish")

def handleCallbackToSlack(callbackToken, event):
    try:
        originalText = event["text"]
        userId = event["user"]
        translatedText = translateTextForUser(originalText, userId)
        if originalText != translatedText:
            chatData = createChatData(callbackToken, event, translatedText)
            ChatUpdater.updateChat(chatData)
        else:
            logging.info("Did not send request to translate: text is same after translation")
    except:
        Logger.logUnexpectedError()

def translateTextForUser(textToTranslate, userId):
    languageToTranslate = UserStorage.getTranslationModeFor(userId)
    action = translationParser.parse_args(["--" + languageToTranslate, textToTranslate])
    if action.scanish:
        return Translator.toSwedish(action.scanish)
    elif action.swedish:
        return Translator.toScanish(action.swedish)
    else:
        return "No text to translate"

def createChatData(callbackToken, event, translatedText):
    return ChatData(
        token = callbackToken, 
        channel = event["channel"], 
        originalText = event["text"], 
        timestamp = event["ts"], 
        userId = event["user"],
        translatedText = translatedText)