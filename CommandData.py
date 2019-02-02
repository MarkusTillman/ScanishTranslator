class CommandData:
    def __init__(self, translatedText, response_url, response_type):
        self.translatedText = translatedText
        self.response_url = response_url
        self.response_type = response_type

    def __eq__(self, other): 
        return self.translatedText == other.translatedText and self.response_url == other.response_url and self.response_type == other.response_type

    def __str__(self):
        return self.translatedText + " " + self.response_url + " " + self.response_type