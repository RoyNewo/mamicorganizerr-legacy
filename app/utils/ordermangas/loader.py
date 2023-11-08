import json


def init():
    global mangas

    configs = "/opt/tachiyomimangaexporter/"
    with open(f'{configs}mangas.json') as mangas_file:
        mangas = json.load(mangas_file)


def save():
    global mangas

    configs = "/opt/tachiyomimangaexporter/"
    with open(f'{configs}mangas.json', "w") as mangas_file:
        json.dump(mangas, mangas_file)
