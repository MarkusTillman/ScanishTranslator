
import shelve
from Storage import Storage 

storage = Storage("user.storage", mode='c', writeback=False)

def isRegisteredUser(user):
    return storage.exists(user)

def registerUser(user, translationMode):
    storage.add(user, translationMode)

def getTranslationModeFor(user):
    return storage.get(user)
