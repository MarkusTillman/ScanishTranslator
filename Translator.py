from bidict import bidict

# TODO: resource files; http://users.student.lth.se/e96pn/skanskaord.html
twoWayDictionary = bidict({
    'skaune': 'skåne',
    'ljuse': 'ljus',
    'ljusena': 'ljusen',
    'unsdag': 'onsdag',
    'uhlsson': 'ohlsson',
    'tacu': 'taco',
    'ust': 'ost',
    'daj': 'dig',
    'e': 'är',
    'me': 'med',
    'dörra': 'dörr',
    'vann': 'vatten',
    'laugom': 'lagom',
    'arbejda': 'arbeta',
    'bloa': 'blöda',
    'chokela': 'choklad',
})
swedishDictionary = {
    'hej': 'haj',
    'mig': 'maj',
    'dig': 'daj',
    'och': 'å',
    'jag': 'ja',
}
scanishDictionary = {
}

def toSwedish(scanishWord):
    return getTranslationUsingDictionaries(twoWayDictionary, scanishDictionary, scanishWord)

def toScanish(swedishWord):
    return getTranslationUsingDictionaries(twoWayDictionary.inv, swedishDictionary, swedishWord)

def getTranslationUsingDictionaries(mainDictionary, fallbackDictionary, word):
    try:
        return mainDictionary[word.lower()]
    except KeyError:
        try:
            return fallbackDictionary[word.lower()]
        except KeyError:
            return word

