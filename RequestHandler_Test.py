import RequestHandler
import logging
import SignatureComputer
import unittest
from unittest.mock import MagicMock, Mock

class TestRequestHandler(unittest.TestCase):
    def testThatSignatureHeaderIsRequired(self):
        request = Mock()
        request.headers = {}
        self.assertRaisesRegex(KeyError, "X-Slack-Signature", RequestHandler.verifySlackRequest, request)
    
    def testThatTimestampHeaderIsRequired(self):
        request = Mock()
        request.headers = {
            "X-Slack-Signature": "abc"
        }
        self.assertRaisesRegex(KeyError, "X-Slack-Request-Timestamp", RequestHandler.verifySlackRequest, request)

    def testThatWarningIsLoggedAndBadRequestIsThrownWhenSignatureDoesNotMatch(self):
        logging.warning = Mock()
        request = Mock()
        request.headers = {
            "X-Slack-Signature": "abc",
            "X-Slack-Request-Timestamp": "123"
        }
        request.get_data = lambda: b"body"
        SignatureComputer.createSlackSignature = MagicMock(return_value = "cbswa")
        
        self.assertRaisesRegex(Exception, "400 Bad Request.*", RequestHandler.verifySlackRequest, request)
        logging.warning.assert_called()
        SignatureComputer.createSlackSignature.reset_mock(return_value = True)

        
