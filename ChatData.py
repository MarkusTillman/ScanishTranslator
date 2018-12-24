class ChatData:
    # Initializer / Instance Attributes
    def __init__(self, token, channel, originalText, timestamp, translatedText):
        self.token = token
        self.channel = channel
        self.originalText = originalText
        self.timestamp = timestamp
        self.translatedText = translatedText