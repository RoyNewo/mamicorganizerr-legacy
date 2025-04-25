import json


def init():
    global secrets
    global mangas
    global history
    global komgabooksid
    global deletefolder
    global tdescargas
    global mensaj
    global mensaj2
    global headers
    global waring
    global ninemangaurls

    configs = "/opt/tachiyomimangaexporter/"
    with open(f'{configs}secrets.json') as secrets_file:
        secrets = json.load(secrets_file)
    with open(f'{configs}mangas.json') as mangas_file:
        mangas = json.load(mangas_file)
    with open(f'{configs}history.json') as history_file:
        history = json.load(history_file)
    with open(f'{configs}komgabooksid.json') as komgabooksid_file:
        komgabooksid = json.load(komgabooksid_file)
    with open(f'{configs}ninemangaurls.json') as ninemangaurls_file:
        ninemangaurls = json.load(ninemangaurls_file)

    deletefolder = "Error while deleting directory"
    tdescargas = "/home/data/Comics/Descargas"
    mensaj = []
    mensaj2 = []

    headers = {
        'User-Agent': "Mozilla/5.0 (Windows NT 10.0; WOW64) Gecko/20100101 Firefox/75"
    }

    waring = '?waring=1'


def save():
    global secrets
    global mangas
    global history
    global ninemangaurls
    global mensaj
    global mensaj2

    configs = "/opt/tachiyomimangaexporter/"
    with open(f'{configs}secrets.json', "w") as secrets_file:
        json.dump(secrets, secrets_file)
    with open(f'{configs}mangas.json', "w") as mangas_file:
        json.dump(mangas, mangas_file)
    with open(f'{configs}history.json', "w") as history_file:
        json.dump(history, history_file)
    with open(f'{configs}ninemangaurls.json', "w") as ninemangaurls_file:
        json.dump(ninemangaurls, ninemangaurls_file)
    mensaj = []
    mensaj2 = []
