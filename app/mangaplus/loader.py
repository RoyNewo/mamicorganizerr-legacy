import json


def init():
    global todosdict
    global secrets
    global mangasnuevos
    global mapeo
    global mangas
    global history
    global deletefolder
    global tdescargas
    global api_url
    global mensaj
    global mensaj2
    global headers
    global anio

    configs = "/opt/tachiyomimangaexportear/"
    with open(configs + "all.json") as todosdic_file:
        todosdict = json.load(todosdic_file)
    with open(configs + "secrets.json") as secrets_file:
        secrets = json.load(secrets_file)
    with open(configs + "mangasnuevos.json") as mangasnuevos_file:
        mangasnuevos = json.load(mangasnuevos_file)
    with open(configs + "mangaplusmapper.json") as mapeo_file:
        mapeo = json.load(mapeo_file)
    with open(configs + "mangas.json") as mangas_file:
        mangas = json.load(mangas_file)
    with open(configs + "history.json") as history_file:
        history = json.load(history_file)

    deletefolder = "Error while deleting directory"
    tdescargas = "/media/cristian/Datos/Comics/Descargas"
    api_url = "https://jumpg-webapi.tokyo-cdn.com/api/"
    mensaj = []
    mensaj2 = []

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36"
    }
    anio = "2022"


def save():
    configs = "/opt/tachiyomimangaexportear/"
    with open(configs + "all.json", "w") as todosdic_file:
        json.dump(todosdict, todosdic_file)
    with open(configs + "secrets.json", "w") as secrets_file:
        json.dump(secrets, secrets_file)
    with open(configs + "mangasnuevos.json", "w") as mangasnuevos_file:
        json.dump(mangasnuevos, mangasnuevos_file)
    with open(configs + "mangaplusmapper.json", "w") as mapeo_file:
        json.dump(mapeo, mapeo_file)
    with open(configs + "mangas.json", "w") as mangas_file:
        json.dump(mangas, mangas_file)
    with open(configs + "history.json", "w") as history_file:
        json.dump(history, history_file)
