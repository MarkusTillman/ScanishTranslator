
import json

fileName = "user.storage"
try:
    registeredUsers = json.load(open(fileName, "r"))
except FileNotFoundError:
    registeredUsers = {}
    open(fileName, "w+").write("{}")

def getFileName():
    return fileName

def isRegisteredUser(userString):
    return userString in registeredUsers

def registerUser(userString, translationMode):
    registeredUsers.update({userString: translationMode})
    file = open(fileName, "w")
    file.write(json.dumps(registeredUsers))

def getTranslationModeFor(userString):
    if isRegisteredUser(userString):
        return registeredUsers[userString]
    return ""
