class Message:
    def __init__(self, date, author, text='', media=False, deleted=False):
        self.date = date
        self.author = author
        self.text = text
        self.media = media
        self.deleted = deleted

    def getEmojis(self):
        pass

    def getLinks(self):
        pass