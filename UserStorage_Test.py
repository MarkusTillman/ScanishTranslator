import UserStorage

class TestRegisterUser:
    def testUnregisteredUser(self):
        assert UserStorage.isRegisteredUser("Unregistered user") == False

    def testThatUserCanBeRegistered(self):
        UserStorage.registerUser("Registered user", "scanish")
        assert UserStorage.isRegisteredUser("Registered user") == True
    
    def testThatSeveralUsersCanBeStored(self):
        UserStorage.registerUser("User Juan", "One")
        UserStorage.registerUser("User Tu", "Two")
        assert UserStorage.isRegisteredUser("User Juan") == True
        assert UserStorage.isRegisteredUser("User Tu") == True

    def testThatTranslationModeDefaultsToNothingWhenUserIsUnregistered(self):
        assert UserStorage.getTranslationModeFor("Unregistered user") == None

    def testFetchTranslationModeForRegisteredUser(self):
        UserStorage.registerUser("Registered user", "swedish")
        assert UserStorage.getTranslationModeFor("Registered user") == "swedish"

    def testThatTranslationModeCanBeOverwritten(self):
        UserStorage.registerUser("Registered user", "valueToBeOverwritten")
        UserStorage.registerUser("Registered user", "newValue")
        assert UserStorage.getTranslationModeFor("Registered user") == "newValue"
