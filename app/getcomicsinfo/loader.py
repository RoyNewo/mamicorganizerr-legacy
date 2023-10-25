import json
import apprise
def init():
    global secrets
    global mangas
    global history
    global komgabooksid
    global deletefolder
    global tdescargas
    global temporal
    global mensaj
    global mensaj2
    global apobj
    global pendingissues
    global annual_issues
    global torrentlist
    global downloadfolder

    configs = "/opt/tachiyomimangaexporter/"
    with open(f'{configs}secrets.json') as secrets_file:
        secrets = json.load(secrets_file)
    with open(f'{configs}mangas.json') as mangas_file:
        mangas = json.load(mangas_file)
    with open(f'{configs}history.json') as history_file:
        history = json.load(history_file)
    with open(f'{configs}komgabooksid.json') as komgabooksid_file:
        komgabooksid = json.load(komgabooksid_file)
    with open(f'{configs}torrentlist.json') as torrentlist_file:
        torrentlist = json.load(torrentlist_file)


    deletefolder = "Error while deleting directory"
    tdescargas = "/media/cristian/Datos/Comics/Descargas"
    temporal = "/media/cristian/Datos/Comics/Descargas/temporal"
    mensaj = []
    mensaj2 = []
    pendingissues = []
    annual_issues = {}
    downloadfolder = "/media/cristian/Datos/Downloads/"

    # Create an Apprise instance
    apobj = apprise.Apprise()

    # Create an Config instance
    config = apprise.AppriseConfig()

    # Add a configuration source:
    config.add('/opt/tachiyomimangaexporter/apprise.yml')

    # Make sure to add our config into our apprise object
    apobj.add(config)

def save():
    global secrets
    global mangas
    global history
    global mensaj
    global mensaj2
    
    configs = "/opt/tachiyomimangaexporter/"
    with open(f'{configs}secrets.json', "w") as secrets_file:
        json.dump(secrets, secrets_file)
    with open(f'{configs}mangas.json', "w") as mangas_file:
        json.dump(mangas, mangas_file)
    with open(f'{configs}history.json', "w") as history_file:
        json.dump(history, history_file)
    with open(f'{configs}torrentlist.json', "w") as torrentlist_file:
        json.dump(torrentlist, torrentlist_file)
    mensaj = []
    mensaj2 = []