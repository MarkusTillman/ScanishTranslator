
from flask import Flask, request

import AuthorizationOperation
import CommandOperation
import EventOperation

app = Flask(__name__)

@app.route("/", methods=["GET"])
def handleUserAuthorizationOfApp():
    return AuthorizationOperation.redirectToSlack(request)

@app.route("/verificationCode", methods=["GET"])
def handleUserAuthorizationCallback():
    return AuthorizationOperation.handleCallbackFromSlack(request)

@app.route("/scanish", methods=["POST"])
def handleSlackCommand():
    return CommandOperation.handle(request)

@app.route("/", methods=["POST"])
def handleSubscribedSlackEvents():
    return EventOperation.handle(request)