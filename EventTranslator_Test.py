import EventTranslator
import UserStorage
import unittest
from unittest.mock import patch

class UnitTests(unittest.TestCase):
    @patch("Logger.logUnexpectedError")
    def testThatExceptionsAreLogged(self, logUnexpectedErrorMock):
        EventTranslator.handleCallbackToSlack("token", {})
        logUnexpectedErrorMock.assert_called()

class IntegrationTests(unittest.TestCase):
    @patch("ChatUpdater.updateChat")
    def testThatTextFieldInEventIsMandatory(self, updateChatMock):
        UserStorage.registerUser("Jane Doe", "scanish")
        event = {
            "text": "Ålahue",
            "user": "Jane Doe",
            "channel": "channel",
            "ts": "timestamp",
        }

        EventTranslator.handleCallbackToSlack("token", event)

        chatDataWithTranslation = EventTranslator.createChatData("token", event, "dumhuvud")
        updateChatMock.assert_called_with(chatDataWithTranslation)