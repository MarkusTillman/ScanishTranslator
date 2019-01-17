import hmac
import hashlib

def createSlackSignature(requestTimestamp, requestBody, binarySigningSecret):
    baseString = ':'.join(["v0", requestTimestamp, requestBody])
    digest = hmac.new(key = binarySigningSecret, msg = baseString.encode("utf-8"), digestmod=hashlib.sha256).hexdigest()
    return "v0=" + digest

def verifySignaturesAreSame(firstSignature, secondSignature):
    return hmac.compare_digest(firstSignature, secondSignature)