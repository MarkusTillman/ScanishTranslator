
import shelve
from Storage import Storage 

storage = Storage("userToken.storage", mode='c', writeback=False)

def hasAuthorized(user):
    return storage.exists(user)

def authorizeUser(user, userToken):
    storage.add(user, userToken)

def getToken(user):
    return storage.get(user)
