import RequestSender
import unittest
from unittest.mock import Mock, patch, ANY
import Logger
import requests

class TestRequestSender(unittest.TestCase):
    @patch("Logger.logOutgoingRequest")
    @patch("requests.post")
    @patch("Logger.logIncomingResponse")
    def testThatHeadersAndBodyAndUrlOfRequestIsLogged(self, logIncomingResponseMock, postMock, logOutgoingRequestMock):
        RequestSender.post(url = "localhost", data = "body", headers = "headers")
        logOutgoingRequestMock.assert_called_with("headers", "body", "localhost")

    @patch("Logger.logOutgoingRequest")
    @patch("requests.post")
    @patch("Logger.logIncomingResponse")
    def testThatRequestItSentToGivenUrl(self, logIncomingResponseMock, postMock, logOutgoingRequestMock):
        RequestSender.post(url = "localhost")
        postMock.assert_called_with(url = "localhost", auth = ANY, data = ANY, json = ANY)

    @patch("Logger.logOutgoingRequest")
    @patch("requests.post")
    @patch("Logger.logIncomingResponse")
    def testThatBasicAuthorizationIsUsedIfUsernameAndPasswordIsProvided(self, logIncomingResponseMock, postMock, logOutgoingRequestMock):
        RequestSender.post(url = "localhost", username="username", password="password")
        basicAuthorization = requests.auth.HTTPBasicAuth("username", "password")
        postMock.assert_called_with(url = ANY, auth = basicAuthorization, data = ANY, json = ANY)

    @patch("Logger.logOutgoingRequest")
    @patch("requests.post")
    @patch("Logger.logIncomingResponse")
    def testThatNoAuthorizationIsUsedIfOnlyUsernameIsProvided(self, logIncomingResponseMock, postMock, logOutgoingRequestMock):
        RequestSender.post(url = "localhost", username="username")
        postMock.assert_called_with(url = ANY, auth = None, data = ANY, json = ANY)

    @patch("Logger.logOutgoingRequest")
    @patch("requests.post")
    @patch("Logger.logIncomingResponse")
    def testThatHeadersAndBodyOfResponseIsLogged(self, logIncomingResponseMock, postMock, logOutgoingRequestMock):
        postMock.return_value = mockResponse("headerData", "content")
        RequestSender.post(url = "localhost")
        logIncomingResponseMock.assert_called_with("headerData", "content")

def mockResponse(headerData, content):
    response = Mock()
    response.headers = headerData
    response.content = content
    return response