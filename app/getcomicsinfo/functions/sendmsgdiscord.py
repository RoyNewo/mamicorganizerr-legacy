from discord import Webhook, RequestsWebhookAdapter
import time


def sendmsg(urlwebhook, mensaj):
    # mensaj.sort()
    msglength = 0
    message = ""
    webhook = Webhook.from_url(
        urlwebhook,
        adapter=RequestsWebhookAdapter(),
    )
    for string in mensaj:
        msglength += len(string)
        if msglength < 2000:
            message += string
        else:
            time.sleep(2)
            webhook.send(message)
            message = string
    time.sleep(2)
    webhook.send(message)


def sendphoto(portrait, urlwebhook):
    portrait += "&random=64"
    webhook = Webhook.from_url(
        urlwebhook,
        adapter=RequestsWebhookAdapter(),
    )
    webhook.send(portrait)