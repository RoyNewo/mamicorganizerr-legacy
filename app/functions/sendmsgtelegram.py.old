import telegram
import time


def sendmsg(token, chatid, mensaj):
    # mensaj.sort()
    msglength = 0
    message = ""
    bot = telegram.Bot(token=token)
    for string in mensaj:
        msglength += len(string)
        if msglength < 4096:
            message += string
        else:
            time.sleep(2)
            bot.sendMessage(chat_id=chatid, text=message)
            message = string
    time.sleep(2)
    bot.sendMessage(chat_id=chatid, text=message)

def sendphoto(portrait, token, chatid):
    portrait += "&random=64"
    bot = telegram.Bot(token=token)
    bot.send_photo(chat_id=chatid, photo=portrait)
