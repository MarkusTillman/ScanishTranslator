
from flask import Flask, request

import AuthorizationOperation
import CommandOperation
import EventOperation

app = Flask(__name__)

@app.route("/", methods=["GET"])
def handleUserAuthorizationOfApp():
    return AuthorizationOperation.handleRedirect(request)

@app.route("/verificationCode", methods=["GET"])
def handleAuthorizationCallback():
    return AuthorizationOperation.handleCallback(request)

@app.route("/scanish", methods=["POST"])
def handleSlackCommand():
    return CommandOperation.handle(request)

@app.route("/", methods=["POST"])
def handleSubscribedSlackEvents():
    return EventOperation.handle(request)