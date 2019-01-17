import AuthorizationOperation
import unittest
from unittest.mock import MagicMock, Mock, patch
import RequestSender
import Logger
import re
import UserAccessTokenStorage

class TestRedirection(unittest.TestCase):

    @patch('RequestSender.redirectRequest')
    def testThatUserIsRedirectedToSlackForAuthorization(self, redirectRequestMock):
        requestMock = Mock()

        AuthorizationOperation.redirectToSlack(requestMock)

        url = redirectRequestMock.call_args[0][1]
        assert "https://slack.com/oauth/authorize" in url

class TestCallbackFromSlack(unittest.TestCase):
    
    @patch('RequestSender.post')
    def testThatCodeInRequestIsSentToSlack(self, postMock): 
        requestMock = mockRequest(verificationCode = "123")
        postMock.return_value = mockResponse()

        AuthorizationOperation.handleCallbackFromSlack(requestMock)
        
        url = postMock.call_args[1]["url"]
        assert re.match(r"https://slack.com/api/oauth.access.*code=123", url) 

    @patch('UserAccessTokenStorage.authorizeUser')
    @patch('RequestSender.post')
    def testThatAccessTokenInResponseIsPersistedForUserWhoAuthorized(self, postMock, authorizeUserMock):
        postMock.return_value = mockResponse("user", "token")
        AuthorizationOperation.handleCallbackFromSlack(mockRequest())
        authorizeUserMock.assert_called_with("user", "token")

    @patch('RequestSender.post')
    def testThatUserReceivesWelcomeMessageUponSuccess(self, postMock):
        postMock.return_value = mockResponse("user", "token")
        assert "Authorization successful" in AuthorizationOperation.handleCallbackFromSlack(mockRequest())
        
    def testThatUserIsToldOfUnknownErrorWhenInternalErrorHappens(self):
        requestWithoutVerificationCode = Mock()
        assert "Unknown error" in AuthorizationOperation.handleCallbackFromSlack(requestWithoutVerificationCode)
    
    @patch('RequestSender.post')
    def testThatNoRequestIsSentToSlackWhenInternalErrorHappens(self, postMock):
        requestWithoutVerificationCode = Mock()
        AuthorizationOperation.handleCallbackFromSlack(requestWithoutVerificationCode)
        postMock.assert_not_called()

    @patch('Logger.logUnexpectedError')
    def testThatErrorsAreLogged(self, logUnexpectedErrorMock):
        requestWithoutVerificationCode = Mock()
        AuthorizationOperation.handleCallbackFromSlack(requestWithoutVerificationCode)
        logUnexpectedErrorMock.assert_called()

def mockRequest(verificationCode=""):
    requestMock = Mock()
    requestMock.args = {"code": verificationCode}
    return requestMock

def mockResponse(userId="", accessToken=""):
    responseMock = Mock()
    responseMock.json = MagicMock(return_value={
        "user_id": userId, 
        "access_token": accessToken
    })
    return responseMock
