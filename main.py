from chatHistory import ChatHistory
from message import Message
import datetime, re




def main():
    # Decode chat export
    history = ChatHistory()
    decodeChatExport(history, filename='deluminaten.txt')
    
    # Do stuff
    history.createWordcloudImages()


def decodeChatExport(history, filename):

    def decodeLine(line):
        if not re.search('^([1-9]|0[1-9]|1[0-9]|2[0-9]|3[0-1])(\.|-|/)([1-9]|0[1-9]|1[0-2])(\.|-|/)([0-9][0-9]|19[0-9][0-9]|20[0-9][0-9])$', line[:8]):
            return None, None, None

        def getDate(line):
            line_split = line.split(' - ')[0].split(', ')

            day = line_split[0][0:2]
            month = line_split[0][3:5]
            year = '20'+line_split[0][6:8]
            hour = line_split[1][0:2]
            minute = line_split[1][3:5]
            date = datetime.datetime(
                year=int(year),
                month=int(month),
                day=int(day),
                hour=int(hour),
                minute=int(minute)
            )
            return date

        def getAuthor(line):
            line_split = line.split(' - ')[1].split(': ')
            if len(line_split) == 1:
                author = 'System'
            else:
                author = line_split[0]
            return author

        def getText(line):
            line_split = line.split(' - ')[1].split(': ')
            if len(line_split) == 1:
                text = line_split[0]
            else:
                text = line_split[1]
            return text

        try:
            date = getDate(line)
            author = getAuthor(line)
            text = getText(line)
        except:
            return None, None, None
        return date, author, text

    with open(filename, encoding='utf-8') as chat_history:
        for line in chat_history:
            date, author, text = decodeLine(line)
            if date and author and text:
                if text == '<Medien ausgeschlossen>\n':
                    history.addMessage(Message(date, author, text, media=True))
                elif text == 'Diese Nachricht wurde gelöscht.\n' or text ==  'Du hast diese Nachricht gelöscht.\n':
                    history.addMessage(Message(date, author, text, media=False, deleted=True))
                else:
                    history.addMessage(Message(date, author, text))
            else:
                history.addToLastMessage(line)

if __name__ == '__main__':
    main()