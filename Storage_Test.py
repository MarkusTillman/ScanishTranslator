from Storage import Storage

class TestStorage:
    storage = Storage("test.storage", mode='c', writeback=False)

    def testThatUnregisteredKeyDoesNotExist(self):
        assert self.storage.exists("Unregistered key") == False

    def testThatValueOfNoneExistingKeyIsNone(self):
        assert self.storage.get("Unregistered key") == None

    def testThatKeyCanBeAdded(self):
        self.storage.add("key", "")
        assert self.storage.exists("key") == True

    def testThatValueOfKeyCanBeFetched(self):
        self.storage.add("key", "value")
        assert self.storage.get("key") == "value"

    def testThatValueOfKeyCanBeOverwritten(self):
        self.storage.add("key", "value")
        self.storage.add("key", "new value")
        assert self.storage.get("key") == "new value"

        
    def testThatSeveralKeysCanBeAdded(self):
        self.storage.add("first key", "first value")
        self.storage.add("second key", "second value")
        assert self.storage.get("first key") == "first value"
        assert self.storage.get("second key") == "second value"