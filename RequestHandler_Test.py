import RequestHandler
import logging
import SignatureComputer
import unittest
from unittest.mock import MagicMock, Mock, patch

class TestRequestHandler(unittest.TestCase):
    def testThatSignatureHeaderIsRequired(self):
        request = Mock()
        request.headers = {}
        request.get_json.return_value = {}
        self.assertRaisesRegex(KeyError, "X-Slack-Signature", RequestHandler.verifySlackRequest, request)
    
    def testThatTimestampHeaderIsRequired(self):
        request = mockRequest(data = b"body", headers = {
            "X-Slack-Signature": "abc"
        })
        self.assertRaisesRegex(KeyError, "X-Slack-Request-Timestamp", RequestHandler.verifySlackRequest, request)

    @patch('logging.warning')
    @patch('SignatureComputer.createSlackSignature')
    def testThatWarningIsLoggedAndBadRequestIsThrownWhenSignatureDoesNotMatch(self, createSlackSignatureMock, warningMock):
        request = mockRequest(data = b"body", headers = {
            "X-Slack-Signature": "abc",
            "X-Slack-Request-Timestamp": "123"
        })
        createSlackSignatureMock.return_value = "cba"
        
        self.assertRaisesRegex(Exception, "400 Bad Request.*", RequestHandler.verifySlackRequest, request)
        warningMock.assert_called()

def mockRequest(headers=None, json={}, data=None):
    request = Mock()
    request.get_json.return_value = json
    request.headers = headers
    request.get_data = lambda: data
    return request
