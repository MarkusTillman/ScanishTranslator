
import shelve
from Storage import Storage 

userStorage = Storage("user.storage", mode='c', writeback=False)

def isRegisteredUser(userString):
    return userStorage.exists(userString)

def registerUser(userString, translationMode):
    userStorage.add(userString, translationMode)

def getTranslationModeFor(userString):
    return userStorage.get(userString)
