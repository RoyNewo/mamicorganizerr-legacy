import mangaplus.loader
import requests
from icecream import ic
from functions import organizer


def listoftitles(groups):
    titles = []
    for group in groups:
        titles.extend(iter(group["titles"]))
    return titles


def mangatype(chaptername):
    if chaptername == "ex":
        ic("mangaespecial")
    elif ',' in chaptername:
        ic("mangadoble")
    else:
        ic(f"{chaptername} es un manga normal")


def main():

    url = f"{mangaplus.loader.api_url}web/web_home?lang=esp&format=json"
    responselast = requests.get(url, headers=mangaplus.loader.headers)
    datalast = responselast.json()

    titles = listoftitles(datalast["success"]["webHomeView"]["groups"])

    for title in titles:
        if title["titleId"] in mangaplus.loader.mapeo:
            mangainfo = mangaplus.loader.mangas[mangaplus.loader.mapeo[title["titleId"]]]
            organizer.folderinit(mangainfo)
            ic(mangainfo["Series"])
            ic(title["chapterName"])
            mangatype(str(title["chapterName"]).replace('#', ''))
