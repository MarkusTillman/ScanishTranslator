import logging

import ChatUpdater
from ChatData import ChatData
import Translator
import UserStorage
import Logger

import RequestSender

def handleCallbackToSlack(callbackToken, event):
    try:
        originalText = event["text"]
        translatedText = Translator.toScanish(originalText)
        if originalText != translatedText:
            chatData = createChatData(callbackToken, event, translatedText)
            ChatUpdater.updateChat(chatData)
        else:
            logging.info("Did not send request to translate: text is same after translation")
    except:
        Logger.logUnexpectedError()

def createChatData(callbackToken, event, translatedText):
    return ChatData(
        token = callbackToken, 
        channel = event["channel"], 
        originalText = event["text"], 
        timestamp = event["ts"], 
        userId = event["user"],
        translatedText = translatedText)

def handleCommandCallbackToSlack(commandData):
    try:
        commandData.translatedText = Translator.toScanish(commandData.originalText)
        ChatUpdater.updateChatWithCommand(commandData)
    except:
        Logger.logUnexpectedError()