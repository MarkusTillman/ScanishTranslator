
import shelve

class Storage:
    def __init__(self, file, mode, writeback):
        self.dictionary = shelve.open(file, mode, writeback) 

    def exists(self, key):
        return key in self.dictionary

    def add(self, key, value):
        self.dictionary.update({key: value})
        self.dictionary.sync()

    def get(self, key):
        return self.dictionary.get(key)

    def close(self):
        self.dictionary.close()