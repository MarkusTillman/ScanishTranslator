import pytest
import Translator

class TestTranslateScanishToSwedish:
    def testThatEmptyStringReturnEmptyString(self):
        assert Translator.toSwedish("") == ""

    def testThatSpaceReturnsSpace(self):
        assert Translator.toSwedish(" ") == " "

    def testThatWordUpperCaseIsTranslated(self):
        assert Translator.toSwedish("SKAUNE").lower() == "skåne"
    
    def testThatWordInLowerCaseIsTranslated(self):
        assert Translator.toSwedish("skaune").lower() == "skåne"

    def testTwoDifferentWordsCanBeTranslatedToTheSameWord(self):
        assert Translator.toSwedish("fubbick") == "dumhuvud"
        assert Translator.toSwedish("ålahue") == "dumhuvud"

    def testThatWordMissingTranslationIsUnchanged(self):
        assert Translator.toSwedish("WordWithoutTranslation") == "WordWithoutTranslation"

    def testThatSeveralWordsCanBeTranslatedAtOnce(self):
        assert Translator.toSwedish("Jävla ålahue jau ei så ked på daj") == "Jävla dumhuvud jag är så trött på dig"

    def testThatSeveralWordsDividedBySpecialCharactersCanBeTranslated(self):
        scanish = "Jävla ålahue; jau. ei. så, ked/putt på daj, o dina päron!"
        assert Translator.toSwedish(scanish) == "Jävla dumhuvud; jag. är. så, trött/irriterad på dig, och dina föräldrar!"

class TestTranslateSwedishToScanish:
    
    def testThatEmptyStringReturnEmptyString(self):
        assert Translator.toScanish("") == ""

    def testThatSpaceReturnsSpace(self):
        assert Translator.toScanish(" ") == " "

    def testThatWordUpperCaseIsTranslated(self):
        assert Translator.toScanish("SKÅNE").lower() == "skaune"
    
    def testThatWordInLowerCaseIsTranslated(self):
        assert Translator.toScanish("skåne").lower() == "skaune"

    def testTwoDifferentWordsCanBeTranslatedToTheSameWord(self):
        assert Translator.toScanish("släpa") == "asa"
        assert Translator.toScanish("dra") == "asa"

    def testThatWordMissingTranslationIsUnchanged(self):
        assert Translator.toScanish("WordWithoutTranslation") == "WordWithoutTranslation"

    def testThatWordWithOnlyOneWayTranslationIsTranslated(self):
        assert Translator.toScanish("hej") == "haj"

    def testThatSeveralWordsCanBeTranslatedAtOnce(self):
        assert Translator.toScanish("Jävla dumhuvud jag är så trött på dig") == "Jävla ålahue jau ei så ked på daj"

    def testThatSeveralWordsDividedBySpecialCharactersCanBeTranslated(self):
        swedish = "Jävla dumhuvud; jag. är. så, trött/irriterad på dig, och dina föräldrar!"
        assert Translator.toScanish(swedish) == "Jävla ålahue; jau. ei. så, ked/putt på daj, o dina päron!"

class TestOtherStuff:
    def testThatSupportedLanguagesAreOnlyScanishAndSwedish(self):
        assert Translator.getSupportedLanguages() == {"scanish", "swedish"}