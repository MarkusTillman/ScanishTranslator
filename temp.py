import hmac
import hashlib
import base64

timestamp = "1545751924"
receivedSignature = "v0=00e49832d2e467dc97057b8b6389d45d89ed3498c7aff154bce2d4b4f97d4299"
body = b''.decode("utf-8")
#body = None
#body = 'command=%sscanish'


#baseString = ':'.join(["v0", timestamp, body]).encode("utf-8")
baseString = f"v0:{timestamp}:{body}".encode('utf-8')
print(baseString)
signingSecret = open("signing.secret", "rb").read()
print(signingSecret)
computedSignature = "v0=" + hmac.new(key = signingSecret, msg = baseString, digestmod=hashlib.sha256).hexdigest()

print("Computed:" + computedSignature)
print("Received:" + receivedSignature)