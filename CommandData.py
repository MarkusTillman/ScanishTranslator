class CommandData:
    def __init__(self, originalText, response_url, response_type, userId, userName, translatedText = ""):
        self.originalText = originalText
        self.translatedText = translatedText
        self.response_url = response_url
        self.response_type = response_type
        self.userId = userId
        self.userName = userName

    def __eq__(self, other): 
        return self.originalText == other.originalText and self.translatedText == other.translatedText and self.response_url == other.response_url and self.response_type == other.response_type and self.userId == other.userId and self.userName == other.userName

    def __str__(self):
        return self.originalText + " " + self.translatedText + " " + self.response_url + " " + self.response_type + " " + self.userId + " " + self.userName