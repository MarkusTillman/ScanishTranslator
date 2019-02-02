
from flask import Flask, request

import AuthorizationOperation
import CommandOperation
import EventOperation
import Logger
import RequestHandler
import Translator

app = Flask(__name__)

@app.route("/", methods=["GET"])
def handleUserAuthorizationOfApp():
    Logger.logIncomingRequest(request.headers, request.get_data())
    return AuthorizationOperation.redirectToSlack(request)

@app.route("/verificationCode", methods=["GET"])
def handleUserAuthorizationCallback():
    Logger.logIncomingRequest(request.headers, request.get_data())
    return AuthorizationOperation.handleCallbackFromSlack(request)

@app.route("/scanish", methods=["POST"])
def handleSlackCommand():
    Logger.logIncomingRequest(request.headers, request.get_data())
    RequestHandler.verifySlackRequest(request)
    return CommandOperation.handle(request)

@app.route("/events", methods=["POST"])
def handleSubscribedSlackEvents():
    Logger.logIncomingRequest(request.headers, request.get_data())
    RequestHandler.verifySlackRequest(request)
    return EventOperation.handle(request)

@app.route("/translate", methods=["POST"])
def handleUserRequest():
    Logger.logIncomingRequest(request.headers, request.get_data())
    return Translator.toScanish(request.data.decode("utf-8"))