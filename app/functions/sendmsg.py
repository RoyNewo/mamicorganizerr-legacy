import apprise
import time

# Create an Apprise instance
apobj = apprise.Apprise()

# Create an Config instance
config = apprise.AppriseConfig()

# Add a configuration source:
config.add('/opt/tachiyomimangaexporter/apprise.yml')

# Make sure to add our config into our apprise object
apobj.add(config)


def sendnewmsg(apptag, mensaj, title):
    msglength = 0
    message = ""
    print(mensaj)
    for string in mensaj:
        msglength += len(string)
        if msglength < 2000:
            message += string
        else:
            time.sleep(2)
            apobj.notify(
                tag=apptag,
                body=message,
                title=title
            )
            message = string
    time.sleep(2)
    apobj.notify(
        tag=apptag,
        body=message,
        title=title
    )
