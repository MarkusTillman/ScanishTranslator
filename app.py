

import logging
from flask import Flask, request

import AuthorizationOperation
import CommandOperation
import EventOperation

app = Flask(__name__)
logging.basicConfig(filename="log.log", level=logging.DEBUG, filemode="w")

def logReceivedRequest(request):
    logging.info("Received: " + str(request.headers) + str(request.get_data()))

@app.route("/", methods=["GET"])
def handleUserAuthorizationOfApp():
    logReceivedRequest(request)
    return AuthorizationOperation.handleRedirect(request)

@app.route("/verificationCode", methods=["GET"])
def handleAuthorizationCallback():
    logReceivedRequest(request)
    return AuthorizationOperation.handleCallback(request)

@app.route("/scanish", methods=["POST"])
def handleSlackCommand():
    logReceivedRequest(request)
    return CommandOperation.handle(request)

@app.route("/", methods=["POST"])
def handleSubscribedSlackEvents():
    logReceivedRequest(request)
    return EventOperation.handle(request)