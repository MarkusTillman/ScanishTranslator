import sys
import argparse

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
    print(F"Translating '{arguments.scanish}' to Swedish")
elif arguments.swedish:
    print(F"Translating '{arguments.swedish}' to Scanish")
else:
    argumentParser.print_usage()