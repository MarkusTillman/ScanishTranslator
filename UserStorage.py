
import shelve
from Storage import Storage 

storage = Storage("user.storage", mode='c', writeback=False)

def isRegisteredUser(user):
    return storage.exists(user)

def registerUser(user):
    storage.add(user, True)

def unregisterUser(user):
    storage.remove(user)