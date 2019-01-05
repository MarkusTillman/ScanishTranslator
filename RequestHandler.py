import hmac
import hashlib
import logging
from flask import request, abort

binarySigningSecret = open("signing.secret", "rb").read()

def verifyRequest(request):
    receivedSignature = request.headers["X-Slack-Signature"]
    timestamp = request.headers["X-Slack-Request-Timestamp"] 
    rawBody = request.get_data()

    baseString = ':'.join(["v0", timestamp, rawBody.decode("utf-8")])
    digest = hmac.new(key = binarySigningSecret, msg = baseString.encode("utf-8"), digestmod=hashlib.sha256).hexdigest()
    computedSignature = "v0=" + digest
    
    if not hmac.compare_digest(computedSignature, receivedSignature):
        logging.warning("Verification failed. Computed signature: " + computedSignature)
        abort(400)