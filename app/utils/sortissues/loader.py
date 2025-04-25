import apprise
import json


def init():
    global secrets
    global deletefolder
    global tdescargas
    global temporal
    global mensaj
    global mensaj2
    global apobj
    global downloadfolder

    configs = "/opt/tachiyomimangaexporter/"
    with open(f'{configs}secrets.json') as secrets_file:
        secrets = json.load(secrets_file)

    deletefolder = "Error while deleting directory"
    tdescargas = "/home/data/Comics/Descargas"
    temporal = "/home/data/Comics/Descargas/temporal"
    mensaj = []
    mensaj2 = []
    downloadfolder = "/home/data/Downloads/"

    # Create an Apprise instance
    apobj = apprise.Apprise()

    # Create an Config instance
    config = apprise.AppriseConfig()

    # Add a configuration source:
    config.add('/opt/tachiyomimangaexporter/apprise.yml')

    # Make sure to add our config into our apprise object
    apobj.add(config)


def save():
    pass
