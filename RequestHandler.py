import logging
from flask import request, abort
import SignatureComputer

binarySigningSecret = open("signing.secret", "rb").read()

def verifySlackRequest(request):
    receivedSignature = request.headers["X-Slack-Signature"]
    timestamp = request.headers["X-Slack-Request-Timestamp"] 
    rawBody = request.get_data()
    computedSignature = SignatureComputer.createSlackSignature(timestamp, rawBody.decode("utf-8"), binarySigningSecret)
    if not SignatureComputer.verifySignaturesAreSame(computedSignature, receivedSignature):
        logging.warning("Verification failed. Computed signature: " + computedSignature)
        abort(400)