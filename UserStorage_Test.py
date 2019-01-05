import UserStorage

class TestRegisterUser:
    def testUnregisteredUser(self):
        assert UserStorage.isRegisteredUser("Unregistered user") == False

    def testThatUserCanBeRegistered(self):
        UserStorage.registerUser("Registered user", "scanish")
        assert UserStorage.isRegisteredUser("Registered user") == True

    def testThatRegisteredUserIsPersisted(self):
        UserStorage.registerUser("Registered user", "tscanish")
        fileWithRegisteredUsers = open(UserStorage.getFileName(), "r")
        assert "Registered user" in fileWithRegisteredUsers.read()

    def testThatTranslationModeDefaultsToNothingWhenUserIsUnregistered(self):
        assert UserStorage.getTranslationModeFor("Unregistered user") == ""

    def testFetchTranslationModeForRegisteredUser(self):
        UserStorage.registerUser("Registered user", "swedish")
        assert UserStorage.getTranslationModeFor("Registered user") == "swedish"