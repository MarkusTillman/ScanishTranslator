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
    
    @patch("UserAccessTokenStorage.hasAuthorized")
    @patch("UserStorage.registerUser")
    @patch("ResponseCreator.createJsonResponse")
    def testThatUserCanRegisterThemselves(self, createJsonResponseMock, registerUserMock, hasAuthorizedMock):
        request = mockRequest("--register", "user id")
        hasAuthorizedMock.return_value = True
        CommandOperation.handle(request)
        registerUserMock.assert_called_with("user id")

    @patch("UserAccessTokenStorage.hasAuthorized")
    @patch("UserStorage.registerUser")
    @patch("ResponseCreator.createJsonResponse")
    def testThatUserIsNotifiedOfSuccessfulRegistrationByReceivingAnImageUrl(self, createJsonResponseMock, registerUserMock, hasAuthorizedMock):
        request = mockRequest("--register", "user id")
        hasAuthorizedMock.return_value = True
        CommandOperation.handle(request)
        createJsonResponseMock.assert_called_with({"response_type": "ephemeral", "attachments": [{"image_url": "https://i.imgur.com/Kyd9VpM.png"}]})

    @patch("UserAccessTokenStorage.hasAuthorized")
    @patch("ResponseCreator.createJsonResponse")
    def testThatUserMustHaveAuthorizedAppBeforeRegisteringLanguageToTranslate(self, createJsonResponseMock, hasAuthorizedMock):
        request = mockRequest("--register", "user id")
        hasAuthorizedMock.return_value = False
        CommandOperation.handle(request)
        createJsonResponseMock.assert_called_with({"response_type": "ephemeral", "text": "You must first authorize the Scanish app at: https://impartial-ibis-5785.dataplicity.io/"})

    @patch("UserAccessTokenStorage.hasAuthorized")
    @patch("UserStorage.unregisterUser")
    @patch("ResponseCreator.createJsonResponse")
    def testThatUserCanUnregisterSelfFromTranslation(self, createJsonResponseMock, unregisterUserMock, hasAuthorizedMock):
        request = mockRequest("--unregister", "user id")
        hasAuthorizedMock.return_value = True
        CommandOperation.handle(request)
        unregisterUserMock.assert_called_with("user id")
        createJsonResponseMock.assert_called_with({"response_type": "ephemeral", "attachments": [{"image_url": "https://i.imgur.com/YYN18jOh.jpg"}]})

    @patch("UserAccessTokenStorage.hasAuthorized")
    @patch("ResponseCreator.createJsonResponse")
    def testThatNonOptionalArgumentIsTranslated(self, createJsonResponseMock, hasAuthorizedMock):
        request = mockRequest("jag är så trött på dig", "user id")
        hasAuthorizedMock.return_value = True
        CommandOperation.handle(request)
        createJsonResponseMock.assert_called_with({"response_type": "in_channel", "text": "jau ei så ked på daj"})

def mockRequest(command, userId = None):
    request = Mock()
    request.form = {
        "text": command,
        "user_id": userId
    }
    return request
