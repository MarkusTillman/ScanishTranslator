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
    @patch("UserStorage.isRegisteredUser")
    @patch("ChatUpdater.updateChat")
    def testThatTextFieldInEventIsMandatory(self, updateChatMock, isRegisteredUserMock):
        isRegisteredUserMock.return_value = True
        event = {
            "text": "dumhuvud",
            "user": "Jane Doe",
            "channel": "channel",
            "ts": "timestamp",
        }

        EventTranslator.handleCallbackToSlack("token", event)

        chatDataWithTranslation = EventTranslator.createChatData("token", event, "ålahue")
        updateChatMock.assert_called_with(chatDataWithTranslation)