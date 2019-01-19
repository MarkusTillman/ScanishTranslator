class ChatData:
    def __init__(self, token, channel, originalText, timestamp, userId, translatedText):
        self.token = token
        self.channel = channel
        self.originalText = originalText
        self.timestamp = timestamp
        self.userId = userId
        self.translatedText = translatedText

    def __eq__(self, other): 
        return self.token == other.token and self.channel == other.channel and self.originalText == other.originalText and self.timestamp == other.timestamp and self.userId == other.userId and self.translatedText == other.translatedText

    def __str__(self):
        return self.token + " " + self.channel + " " + self.originalText + " " + self.timestamp + " " + self.userId + " " + self.translatedText