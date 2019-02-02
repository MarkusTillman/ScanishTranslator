import EventOperation
import unittest
from unittest.mock import Mock, patch
import CallbackHandler

class TestEventOperation(unittest.TestCase):
    
    @patch("ResponseCreator.createJsonResponse")
    def testThatChallengeInRequestIsReturnedInResponseIfSet(self, createJsonResponseMock):
        challengeRequest = mockRequest({ "challenge" : "challenge data" })
        EventOperation.handle(challengeRequest)
        createJsonResponseMock.assert_called_with({ "challenge" : "challenge data" })

    @patch("Logger.logUnexpectedError")
    def testThatExceptionDuringHandlingReturnsEmptyResponse(self, logUnexpectedErrorMock):
        assert EventOperation.handle(None) == ""
        logUnexpectedErrorMock.assert_called()

    @patch("UserStorage.isRegisteredUser")
    @patch("_thread.start_new_thread")
    def testRequestWithRequiredValuesStartsnewThreadForTranslating(self, start_new_threadMock, isRegisteredUserMock):
        event = {
            "user": "user",
            "type": "message",
            "text": "ålahue"
        }
        isRegisteredUserMock.return_value = True
        requestWithRequiredValues = mockRequest({ 
            "token": "token",
            "event": event
        })

        assert EventOperation.handle(requestWithRequiredValues) == ""

        start_new_threadMock.assert_called_with(CallbackHandler.handleCallbackToSlack, ("token", event))

    @patch("_thread.start_new_thread")
    def testThatEventSubtypesAreUnhandled(self, start_new_threadMock):
        event = {
            "user": "user",
            "type": "message",
            "text": "ålahue",
            "subtype": "updated"
        }
        requestWithEventSubType = mockRequest({ 
            "token": "token",
            "event": event
        })

        EventOperation.handle(requestWithEventSubType)

        start_new_threadMock.assert_not_called()

def mockRequest(jsonData = {}):
    request = Mock()
    request.get_json.return_value = jsonData
    return request
