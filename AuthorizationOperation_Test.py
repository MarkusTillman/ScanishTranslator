import AuthorizationOperation
from unittest.mock import MagicMock, Mock
import RequestSender
import Logger
import re
import UserAccessTokenStorage

class TestRedirection:
    def testThatUserIsRedirectedToSlackForAuthorization(self):
        requestMock = Mock()
        RequestSender.redirectRequest = MagicMock()

        AuthorizationOperation.redirectToSlack(requestMock)

        url = RequestSender.redirectRequest.call_args[0][1]
        assert "https://slack.com/oauth/authorize" in url

class TestCallbackFromSlack:
    def testThatCodeInRequestIsSentToSlack(self): 
        requestMock = mockRequest(verificationCode = "123")
        responseMock = mockResponse()
        RequestSender.post = MagicMock(return_value = responseMock)

        AuthorizationOperation.handleCallbackFromSlack(requestMock)
        
        url = RequestSender.post.call_args[1]["url"]
        assert re.match(r"https://slack.com/api/oauth.access.*code=123", url) 

    def testThatAccessTokenInResponseIsPersistedForUserWhoAuthorized(self):
        requestMock = mockRequest()
        responseMock = mockResponse("user", "token")
        RequestSender.post = MagicMock(return_value = responseMock)
        UserAccessTokenStorage.authorizeUser = MagicMock()

        AuthorizationOperation.handleCallbackFromSlack(requestMock)

        UserAccessTokenStorage.authorizeUser.assert_called_with("user", "token")

    def testThatUserReceivesWelcomeMessageUponSuccess(self):
        requestMock = mockRequest()
        assert "Authorization successful" in AuthorizationOperation.handleCallbackFromSlack(requestMock)
        
    def testThatUserIsToldOfUnknownErrorWhenInternalErrorHappens(self):
        requestWithoutVerificationCode = Mock()
        assert "Unknown error" in AuthorizationOperation.handleCallbackFromSlack(requestWithoutVerificationCode)
    
    def testThatNoRequestIsSentToSlackWhenInternalErrorHappens(self):
        requestWithoutVerificationCode = Mock()
        RequestSender.post = MagicMock()

        AuthorizationOperation.handleCallbackFromSlack(requestWithoutVerificationCode)

        RequestSender.post.assert_not_called()

    def testThatErrorsAreLogged(self):
        requestWithoutVerificationCode = Mock()
        Logger.logUnexpectedError = MagicMock()

        AuthorizationOperation.handleCallbackFromSlack(requestWithoutVerificationCode)

        Logger.logUnexpectedError.assert_called()

    @classmethod
    def tearDownClass(cls):
        RequestSender.redirectRequest.reset_mock(return_value = True, side_effect = True)
        RequestSender.post.reset_mock(return_value = True, side_effect = True)
        UserAccessTokenStorage.authorizeUser.reset_mock(side_effect = True)

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
