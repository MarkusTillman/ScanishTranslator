import sys
import argparse
import Translator

argumentParser = argparse.ArgumentParser()
argumentParser.add_argument("--scanish", help="Scanish text to be translated to Swedish")
argumentParser.add_argument("--swedish", help="Swedish text to be translated to Scanish")

def argumentsAreFromCommandLine():
    return len(sys.argv) > 1

def getTextFromRequest():
    return "--scanish scanish".split() # TODO: temporary.

if argumentsAreFromCommandLine():
    textToParse = None
else:
    textToParse = getTextFromRequest()

arguments = argumentParser.parse_args(textToParse)

if arguments.scanish:
    print(Translator.toSwedish(arguments.scanish))
elif arguments.swedish:
    print(Translator.toScanish(arguments.swedish))
else:
    argumentParser.print_usage()
