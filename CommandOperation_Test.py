import CommandOperation
import unittest
from unittest.mock import patch, Mock

class TestRegisterCommand(unittest.TestCase):

    @patch("Logger.logUnexpectedError")
    @patch("ResponseCreator.createJsonResponse")
    def testThatUnrecognizedCommandReturnsHowToUseTheOperationInTheTextField(self, createJsonResponseMock, logUnexpectedErrorMock):
        request = mockRequest("--unrecognizedCommand")
        CommandOperation.handle(request)
        assert "usage" in createJsonResponseMock.call_args[0][0]["text"]
    
    @patch("UserStorage.registerUser")
    @patch("ResponseCreator.createJsonResponse")
    def testThatUserAndTheirRequestTranslationModeIsRegistered(self, createJsonResponseMock, registerUserMock):
        request = mockRequest("--register scanish", "user id")
        CommandOperation.handle(request)
        registerUserMock.assert_called_with("user id", "scanish")

    @patch("UserStorage.registerUser")
    @patch("ResponseCreator.createJsonResponse")
    def testThatUserIsNotifiedOfSuccessfulRegistrationByReceivingAnImageUrl(self, createJsonResponseMock, registerUserMock):
        request = mockRequest("--register scanish", "user id")
        CommandOperation.handle(request)
        createJsonResponseMock.assert_called_with({"response_type": "ephemeral", "attachments": [{"image_url": "https://i.imgur.com/Kyd9VpM.png"}]})

def mockRequest(command, userId = None):
    request = Mock()
    request.form = {
        "text": command,
        "user_id": userId
    }
    return request
