from discord import Webhook
import time
import aiohttp


async def sendmsg(urlwebhook, mensaj):
    # mensaj.sort()
    msglength = 0
    message = ""
    async with aiohttp.ClientSession() as session:
        webhook = Webhook.from_url(
            urlwebhook,
            session=session,
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
        await webhook.send(message)


async def sendphoto(portrait, urlwebhook):
    portrait += "&random=64"
    async with aiohttp.ClientSession() as session:
        webhook = Webhook.from_url(
            urlwebhook,
            session=session,
        )
        webhook.send(portrait)