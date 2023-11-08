import json


def init():
    global mangaplusmapper
    global mangas
    global history
    global komgabooksid

    configs = "/opt/tachiyomimangaexporter/"
    with open(f'{configs}mangaplusmapper.json') as mangaplusmapper_file:
        mangaplusmapper = json.load(mangaplusmapper_file)
    with open(f'{configs}mangas.json') as mangas_file:
        mangas = json.load(mangas_file)
    with open(f'{configs}history.json') as history_file:
        history = json.load(history_file)
    with open(f'{configs}komgabooksid.json') as komgabooksid_file:
        komgabooksid = json.load(komgabooksid_file)


def save():
    global mangaplusmapper
    global mangas
    global history
    global komgabooksid

    configs = "/opt/tachiyomimangaexporter/"
    with open(f'{configs}mangaplusmapper.json', "w") as mangaplusmapper_file:
        json.dump(mangaplusmapper, mangaplusmapper_file)
    with open(f'{configs}mangas.json', "w") as mangas_file:
        json.dump(mangas, mangas_file)
    with open(f'{configs}history.json', "w") as history_file:
        json.dump(history, history_file)
    with open(f'{configs}komgabooksid.json', "w") as komgabooksid_file:
        json.dump(komgabooksid, komgabooksid_file)
