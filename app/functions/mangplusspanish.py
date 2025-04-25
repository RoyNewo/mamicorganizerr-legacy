import requests
import json
import unicodedata
import organizer as organizar

rutahistorial = "/opt/tachiyomimangaexporter/history.json"
anio = "2021"
api_url = "https://jumpg-webapi.tokyo-cdn.com/api/"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36"
}


def elimina_tildes(cadena):
    return "".join(
        (
            c
            for c in unicodedata.normalize("NFD", cadena)
            if unicodedata.category(c) != "Mn"
        )
    )


def spanishjson():
    url = api_url + "title_list/all?format=json"
    responsemanga = requests.get(url, headers=headers)
    datamanga = responsemanga.json()
    mangasspanish = []
    caracteres = '<>:"/\|?*'
    for manga2 in datamanga["success"]["allTitlesView"]["titles"]:
        if "language" in manga2:
            if manga2["language"] == "SPANISH":
                nombremanga = str(manga2["name"])
                for char in caracteres:
                    nombremanga = nombremanga.replace(char, "")
                source = (
                    "/home/data/Comics/Tachiyomi/MANGA Plus by SHUEISHA (ES)/"
                    + nombremanga
                )
                funcion = "MANGA Plus by SHUEISHA (ES)"
                provider = "MANGA Plus by SHUEISHA (ES)"
                output = (
                    "/home/data/Comics/Reader/Shueisha/"
                    + nombremanga
                    + " ("
                    + anio
                    + ")"
                )
                name = nombremanga + " (" + anio + ") Issue #"
                series = nombremanga
                mangaid = manga2["titleId"]
                portrait = manga2["portraitImageUrl"]

                mangasspanish.append(
                    {
                        source: {
                            "destino": output,
                            "name": name,
                            "funcion": funcion,
                            "provider": provider,
                            "slug": "undefined",
                            "Series": series,
                            "Volume": anio,
                            "Publisher": "Shueisha",
                            "mangaid": mangaid,
                            "portrait": portrait,
                        }
                    }
                )
    file = {"mangasspanish": mangasspanish}
    with open(
        "/opt/tachiyomimangaexporter/mangasspanish.json", "w", encoding="utf8"
    ) as outfile:
        json.dump(file, outfile, ensure_ascii=False)


def main():

    with open("/opt/tachiyomimangaexporter/mangasspanish.json") as json_file:
        mangas = json.load(json_file)

    for manga in mangas["mangasspanish"]:
        organizar.folderinit(manga)
        url = api_url + "title_detail?title_id=" + manga["mangaid"] + "&format=json"


if __name__ == "__main__":
    main()
