import mangaplus.loader
import requests
from icecream import ic

def getnamefromchapters(negaindice, chapters):
    contador = 0
    while str(chapters[negaindice]["name"]).replace('#', '') == 'ex':
        negaindice -= 1
        contador += 1
    return negaindice, contador

def specialmanga(chapterid):
    url = f"{mangaplus.loader.api_url}manga_viewer?chapter_id={chapterid}&split=no&img_quality=super_high&format=json"


    responsechapter = requests.get(url, headers=mangaplus.loader.headers)
    datachapter = responsechapter.json()

    chapters = datachapter["success"]["mangaViewer"]["chapters"]

    for idx, val in enumerate(chapters):
        if str(val["chapterId"]) == chapterid:
            ic(idx, val)
            ic(
                "Es un capitulo especial y el inidice va a ser: "
                + chapters[int(idx) - 1]["name"]
            )
            negaindice = int(idx)
    if len(chapters) <= 1:
        return chapters[negaindice]["name"] + .1


    index, contador = getnamefromchapters(negaindice, chapters)
    return (
        chapters[index]["name"]
        + "."
        + str(contador)
    )