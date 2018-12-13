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
        assert Translator.toScanish("och") == "å"
