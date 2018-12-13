from bidict import bidict
import json

twoWayDictionary = bidict(json.load(open("twoWay.dict", encoding="utf-8")))
swedishDictionary = json.load(open("swedishToScanish.dict", encoding="utf-8"))
scanishDictionary = json.load(open("scanishToSwedish.dict", encoding="utf-8"))

def toSwedish(scanishText):
    if scanishText.isspace():
        return scanishText

    return translateText(twoWayDictionary, scanishDictionary, scanishText)

def toScanish(swedishText):
    if swedishText.isspace():
        return swedishText

    return translateText(twoWayDictionary.inv, swedishDictionary, swedishText)

def translateText(mainDictionary, fallbackDictionary, textToTranslate):
    strippedText = textToTranslate.strip()
    translatedText = ""
    for word in strippedText.split(" "):
        potentiallyTranslatedWord = tryToTranslateWord(mainDictionary, fallbackDictionary, word)
        translatedText += F"{potentiallyTranslatedWord} "
    return translatedText.rstrip()

def tryToTranslateWord(mainDictionary, fallbackDictionary, wordToTranslate):
    try:
        return mainDictionary[wordToTranslate.lower()]
    except KeyError:
        try:
            return fallbackDictionary[wordToTranslate.lower()]
        except KeyError:
            return wordToTranslate