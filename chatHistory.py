from stoppwoerter import stoppWoerter, stoppWoerterCustom
from wordcloud import WordCloud

import re

class ChatHistory:
    def __init__(self):
        self.messages = []

    def getAuthors(self):
        authors = []
        for m in self.messages:
            if m.author not in authors:
                authors.append(m.author)
        return authors

    def addMessage(self, message):
        self.messages.append(message)

    def addToLastMessage(self, text):
        self.messages[-1].text += text

    def createWordcloudImages(self):
        for author in self.getAuthors():
            print('Create image for {}...'.format(author))
            try:
                wordcloud = WordCloud(width=1600, height=900, background_color="white").generate(self.getWordsForWordCloud(author=author))
                wordcloud.to_file(filename='img/{}.png'.format(author.strip()))
            except:
                pass

    def getNumberOfMessages(self, author):
        return sum(m.author == author for m in self.messages)

    def getMessagesFrom(self, author):
        if author:
            return list(filter(lambda x: x.author == author , self.messages))
        else:
            return self.messages

    def getWordCount(self, author):
        counts = dict()
        if author:
            messages = self.getMessagesFrom(author)
        else:
            messages = self.messages
        for message in messages:
            if not message.media:
                words = message.text.split()
                for word in words:
                    word = word.lower()
                    if word in stoppWoerter:
                        continue
                    else:
                        if word in counts:
                            counts[word] += 1
                        else:
                            counts[word] = 1
        return sorted(counts.items(), key=lambda x: x[1], reverse=True)
    

    def getWordsForWordCloud(self, author=None):
        if author:
            messages = self.getMessagesFrom(author)
        else:
            messages = self.messages
        words = []
        clean = []
        for message in messages:
            if not message.media and not message.deleted:
                for word in message.text.split():
                    word = word.lower()
                    if word in stoppWoerter or word in stoppWoerterCustom or word.startswith('https://') or word.startswith('dich…') or len(word) < 3:
                        continue
                    else:
                        words.append(word)
        words = re.sub(r"[,.;@#?!&$*]+\ *", " ", ' '.join(words))

        for word in words.split(' '):
            if word not in stoppWoerter:
                clean.append(word)
        return ' '.join(clean)

    def word_count(self, words):
        counts = dict()
        words = words.split()

        for word in words:
            if word in counts:
                counts[word] += 1
            else:
                counts[word] = 1

        return counts