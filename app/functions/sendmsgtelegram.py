import telegram
import time
import mangaplus.loader


def sendmsg(token, chatid):
    mangaplus.loader.mensaj.sort()
    msglength = 0
    message = ""
    bot = telegram.Bot(token=token)
    for string in mangaplus.loader.mensaj:
        msglength += len(string)
        if msglength < 4096:
            message += string
        else:
            time.sleep(2)
            bot.sendMessage(chat_id=chatid, text=message)
            message = string
    time.sleep(2)
    bot.sendMessage(chat_id=chatid, text=message)
    mangaplus.loader.mensaj = []

def sendphoto(portrait, token, chatid):
    portrait += "&random=64"
    bot = telegram.Bot(token=token)
    bot.send_photo(chat_id=chatid, photo=portrait)
