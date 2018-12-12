from bidict import bidict
import json

twoWayDictionary = bidict(json.load(open("twoWay.dict", encoding="utf-8")))
swedishDictionary = json.load(open("swedishToScanish.dict", encoding="utf-8"))
scanishDictionary = json.load(open("scanishToSwedish.dict", encoding="utf-8"))

def toSwedish(scanishWord):
    return getTranslationUsingDictionaries(twoWayDictionary, scanishDictionary, scanishWord)

def toScanish(swedishWord):
    return getTranslationUsingDictionaries(twoWayDictionary.inv, swedishDictionary, swedishWord)

def getTranslationUsingDictionaries(mainDictionary, fallbackDictionary, wordToTranslate):
    try:
        return mainDictionary[wordToTranslate.lower()]
    except KeyError:
        try:
            return fallbackDictionary[wordToTranslate.lower()]
        except KeyError:
            return wordToTranslate

