import mangaplus.loader
import mangaplus.checkmapper
import requests
from icecream import ic

def postermangaplus(manga, url):
    image = requests.get(url, headers=mangaplus.loader.headers)
    imagesave = str(manga["destino"] + "/poster.jpg")
    with open(imagesave, "wb") as f:
        f.write(image.content)


def main():
    if mangaplus.checkmapper.checkmapper():
        for mapeo in mangaplus.loader.mapeo:
            jsonurl = (
                mangaplus.loader.api_url
                + "title_detailV3?title_id="
                + mapeo
                + "&format=json"
            )
            responsetodos = requests.get(jsonurl, headers=mangaplus.loader.headers)
            datamanga = responsetodos.json()
            if "success" in datamanga:
                ic(datamanga["success"]["titleDetailView"]["title"]["portraitImageUrl"])
                postermangaplus(mangaplus.loader.mangas[mangaplus.loader.mapeo[mapeo]], datamanga["success"]["titleDetailView"]["title"]["portraitImageUrl"], )
            else:
                ic(mangaplus.loader.mapeo[mapeo])
            
