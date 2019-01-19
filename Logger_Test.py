import Logger
import unittest
from unittest.mock import patch

class TestLogging(unittest.TestCase):
    @patch("logging.error")
    def testThatSystemExceptionIsLogged(self, errorMock):
        try:
            raise ValueError("Test logging")
        except:
            Logger.logUnexpectedError()
            self.assertRegex(str(errorMock.call_args), ".*ValueError.*Test.*")
