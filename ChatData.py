class ChatData:
    def __init__(self, token, channel, originalText, timestamp, userId, translatedText):
        self.token = token
        self.channel = channel
        self.originalText = originalText
        self.timestamp = timestamp
        self.userId = userId
        self.translatedText = translatedText