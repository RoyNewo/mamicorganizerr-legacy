import mangaplus.loader
import requests
from functions import sendmsg


anio = "2025"


def savenewmangas(sourcefolder, targetfolder, name, funcion, provider, series, mangaid, portrait):
    mangaplus.loader.mangasnuevos["new"].append(
        {
            sourcefolder: {
                "destino": targetfolder,
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


def sourceprovider(webmanga):
    if "language" in webmanga:
        if webmanga["language"] == "SPANISH":
            sourcefolder = (
                "/home/data/Comics/Tachiyomi/MANGA Plus by SHUEISHA (ES)/"
                + webmanga["name"]
            )
            funcion = "MANGA Plus by SHUEISHA (ES)"
            provider = "MANGA Plus by SHUEISHA (ES)"
    else:
        sourcefolder = (
            "/home/data/Comics/Tachiyomi/MANGA Plus by SHUEISHA (EN)/"
            + webmanga["name"]
        )
        funcion = "MANGA Plus by SHUEISHA (EN)"
        provider = "MANGA Plus by SHUEISHA (EN)"
    return sourcefolder, funcion, provider


def preparemsg(mangaid):
    url = mangaplus.loader.api_url + \
        "title_detail?title_id=" + str(mangaid) + "&format=json"
    responsedetail = requests.get(url, headers=mangaplus.loader.headers)
    datadetail = responsedetail.json()
    mangaplus.loader.mensaj = [
        'There is a new manga in MangaPlus\n\n',
        (
            "Nombre: "
            + datadetail["success"]["titleDetailView"]["title"]["name"]
            + "\n\n"
        ),
        (
            "Autor: "
            + datadetail["success"]["titleDetailView"]["title"]["author"]
            + "\n\n"
        ),
        (
            "Descripcion: "
            + datadetail["success"]["titleDetailView"]["overview"]
            + "\n\n"
        ),
    ]

    if "isSimulReleased" in datadetail["success"]["titleDetailView"]:
        mangaplus.loader.mensaj.append("Simulrelease\n\n")
    else:
        mangaplus.loader.mensaj.append("No Simulrelease\n\n")
    


def main():

    # hacemos la peticion a la web con la lista de todos los mangas y los guardamos en el diccionario datamanga
    url = f'{mangaplus.loader.api_url}title_list/all?format=json'
    responsemanga = requests.get(url, headers=mangaplus.loader.headers)
    webdatamanga = responsemanga.json()

    for webmanga in webdatamanga["success"]["allTitlesView"]["titles"]:
        if webmanga not in mangaplus.loader.todosdict["success"]["allTitlesView"]["titles"]:
            targetfolder = (
                "/home/data/Comics/Reader/Shueisha/"
                + webmanga["name"]
                + " ("
                + mangaplus.loader.anio
                + ")"
            )
            name = webmanga["name"] + " (" + anio + ") Issue #"
            series = webmanga["name"]
            mangaid = webmanga["titleId"]
            portrait = webmanga["portraitImageUrl"]
            sourcefolder, funcion, provider = sourceprovider(webmanga)
            savenewmangas(sourcefolder, targetfolder, name,
                          funcion, provider, series, mangaid, portrait)
            preparemsg(mangaid)
            # a corregir por que creo que no funcionaba antes y ahora hay que meterlo todo en un metodo con apprsie
            # if mangaplus.loader.secrets["telegram"] == "True":
            #     sendmsgtelegram.sendmsg(mangaplus.loader.secrets["token"], mangaplus.loader.secrets["chatid"])
            #     sendmsgtelegram.sendphoto(portrait, mangaplus.loader.secrets["token"], mangaplus.loader.secrets["chatid"])
            # if mangaplus.loader.secrets["discord"] == "True":
            #     sendmsgdiscord.sendmsg(mangaplus.loader.secrets["disdcordwebhook"])
            #     sendmsgdiscord.sendphoto(portrait, mangaplus.loader.secrets["disdcordwebhook"])
