import SignatureComputer

class TestSlackSignature:
    def testSignaturePrefix(self):
        assert SignatureComputer.createSlackSignature("timestamp", "body", b"secret").startswith("v0=")

class TestSignatures:
    def testThatIdenticalSignatureIsRecognizedAsTheSameSignature(self):
        assert SignatureComputer.verifySignaturesAreSame("123", "123") == True

    def testThatDifferentSignaturesAreRecognizedAsDifferent(self):
        assert SignatureComputer.verifySignaturesAreSame("123", "abc") == False