import json
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

    configs = "/opt/tachiyomimangaexporter/"
    with open(f'{configs}secrets.json') as secrets_file:
        secrets = json.load(secrets_file)
    with open(f'{configs}mangas.json') as mangas_file:
        mangas = json.load(mangas_file)
    with open(f'{configs}history.json') as history_file:
        history = json.load(history_file)
    with open(f'{configs}komgabooksid.json') as komgabooksid_file:
        komgabooksid = json.load(komgabooksid_file)


    deletefolder = "Error while deleting directory"
    tdescargas = "/media/cristian/Datos/Comics/Descargas"
    temporal = "/media/cristian/Datos/Comics/Descargas/temporal"
    mensaj = []
    mensaj2 = []

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
    mensaj = []
    mensaj2 = []