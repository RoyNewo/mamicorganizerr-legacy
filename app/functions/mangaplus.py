from re import T
import requests
import json
import telegram
import time
import os
import shutil
from icecream import ic
import functions.organizer as organizar
import urllib.request
from discord import Webhook, RequestsWebhookAdapter


api_url = "https://jumpg-webapi.tokyo-cdn.com/api/"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36"
}
rutahistorial = "/opt/tachiyomimangaexporter/history.json"
anio = "2022"


def downloadchapter(path, chapterid, name, number):
    url = (
        api_url
        + "manga_viewer?chapter_id="
        + str(chapterid)
        + "&split=no&img_quality=super_high&format=json"
    )
    responsechapter = requests.get(url, headers=headers)
    datachapter = responsechapter.json()
    if "error" in datachapter:
        return False

    dfolder = path + "/" + name + number
    if not os.path.exists(dfolder):
        os.makedirs(dfolder)
    for chapter in range(len(datachapter["success"]["mangaViewer"]["pages"])):
        if "mangaPage" in datachapter["success"]["mangaViewer"]["pages"][chapter]:
            imgpath = dfolder + "/" + "{:0>3}".format(chapter) + ".jpg"
            imgdecrypt(
                datachapter["success"]["mangaViewer"]["pages"][chapter]["mangaPage"][
                    "imageUrl"
                ],
                imgpath,
                datachapter["success"]["mangaViewer"]["pages"][chapter]["mangaPage"][
                    "encryptionKey"
                ],
            )
    return True


def imgdecrypt(imgurl, imgpath, hexkey):
    try:
        url = imgurl

        # take path of image as output path
        path = imgpath

        resp = requests.get(url, headers=headers)
        data = bytearray(resp.content)
        key = bytes.fromhex(hexkey)
        a = len(key)
        for s in range(len(data)):
            data[s] ^= key[s % a]

        with open(path, "wb") as fin:
            # writing decryption data in image
            fin.write(data)
    except Exception:
        print("Error caught : ", Exception.__name__)


def nuevosmangas():
    with open("/opt/tachiyomimangaexporter/all.json") as json_file:
        todosdict = json.load(json_file)
    with open("/opt/tachiyomimangaexporter/secrets.json") as json_file2:
        secrets = json.load(json_file2)
    with open("/opt/tachiyomimangaexporter/mangasnuevos.json") as json_file2:
        mangasnuevos = json.load(json_file2)
    todoslist = [
        {manga["titleId"]: manga["name"]}
        for manga in todosdict["success"]["allTitlesView"]["titles"]
    ]

    url = api_url + "title_list/all?format=json"
    responsemanga = requests.get(url, headers=headers)
    datamanga = responsemanga.json()

    for manga2 in datamanga["success"]["allTitlesView"]["titles"]:
        tempdict = {manga2["titleId"]: manga2["name"]}

        if tempdict not in todoslist:
            if "language" in manga2:
                if manga2["language"] == "SPANISH":
                    source = (
                        "/media/cristian/Datos/Comics/Tachiyomi/MANGA Plus by SHUEISHA (ES)/"
                        + manga2["name"]
                    )
                    funcion = "MANGA Plus by SHUEISHA (ES)"
                    provider = "MANGA Plus by SHUEISHA (ES)"
                    enviar = True
                else:
                    enviar = False
            else:
                source = (
                    "/media/cristian/Datos/Comics/Tachiyomi/MANGA Plus by SHUEISHA (EN)/"
                    + manga2["name"]
                )
                funcion = "MANGA Plus by SHUEISHA (EN)"
                provider = "MANGA Plus by SHUEISHA (EN)"
                enviar = True
            output = (
                "/media/cristian/Datos/Comics/Reader/Shueisha/"
                + manga2["name"]
                + " ("
                + anio
                + ")"
            )
            name = manga2["name"] + " (" + anio + ") Issue #"
            series = manga2["name"]
            mangaid = manga2["titleId"]
            portrait = manga2["portraitImageUrl"]

            if enviar:
                mangasnuevos["nuevos"].append(
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
                mensaje = (
                    "Se ha detectado un nuevo manga en la aplicacione MangaPlus\n\n"
                )
                url = api_url + "title_detail?title_id=" + str(mangaid) + "&format=json"
                responsedetail = requests.get(url, headers=headers)
                datadetail = responsedetail.json()
                msg = (
                    "Nombre: "
                    + datadetail["success"]["titleDetailView"]["title"]["name"]
                    + "\n\n"
                )
                mensaje += msg
                msg = (
                    "Autor: "
                    + datadetail["success"]["titleDetailView"]["title"]["author"]
                    + "\n\n"
                )
                mensaje += msg
                msg = (
                    "Descripcion: "
                    + datadetail["success"]["titleDetailView"]["overview"]
                    + "\n\n"
                )
                mensaje += msg
                if "isSimulReleased" in datadetail["success"]["titleDetailView"]:
                    mensaje += "Simulrelease\n\n"
                else:
                    mensaje += "No Simulrelease\n\n"

                bot = telegram.Bot(token=secrets["token"])
                bot.sendMessage(chat_id=secrets["chatid"], text=mensaje)
                webhook = Webhook.from_url(
                    secrets["disdcordwebhook"],
                    adapter=RequestsWebhookAdapter(),
                )
                webhook.send(mensaje)
                ic(portrait)
                portrait = portrait + "&random=64"
                with urllib.request.urlopen(portrait) as response:
                    info = response.info()
                    print(info.get_content_type())  # -> text/html
                    print(info.get_content_maintype())  # -> text
                    print(info.get_content_subtype())  # -> html
                bot.send_photo(chat_id=secrets["chatid"], photo=portrait)
                webhook.send(portrait)
                time.sleep(2)
    ic()
    with open("/opt/tachiyomimangaexporter/all.json", "w") as outfile:
        json.dump(datamanga, outfile)
    with open("/opt/tachiyomimangaexporter/mangasnuevos.json", "w") as outfile:
        json.dump(mangasnuevos, outfile)


def ultimosmangas(mensaj, mensaj2):
    with open("/opt/tachiyomimangaexporter/mangaplusmapper.json") as json_file:
        mapeo = json.load(json_file)
    with open("/opt/tachiyomimangaexporter/mangas.json") as json_file2:
        mangas = json.load(json_file2)
    with open(rutahistorial) as json_file3:
        history = json.load(json_file3)
    url = api_url + "web/web_home?lang=esp&format=json"
    responseultimos = requests.get(url, headers=headers)
    dataultimos = responseultimos.json()
    for groupnumber in range(len(dataultimos["success"]["webHomeView"]["groups"])):
        for titlenumber in range(
            len(dataultimos["success"]["webHomeView"]["groups"][groupnumber]["titles"])
        ):
            if (
                str(
                    dataultimos["success"]["webHomeView"]["groups"][groupnumber][
                        "titles"
                    ][titlenumber]["title"]["titleId"]
                )
                in mapeo
            ):
                organizar.folderinit(
                    mangas[
                        mapeo[
                            str(
                                dataultimos["success"]["webHomeView"]["groups"][
                                    groupnumber
                                ]["titles"][titlenumber]["title"]["titleId"]
                            )
                        ]
                    ]
                )
                ic(
                    mangas[
                        mapeo[
                            str(
                                dataultimos["success"]["webHomeView"]["groups"][
                                    groupnumber
                                ]["titles"][titlenumber]["title"]["titleId"]
                            )
                        ]
                    ]["Series"]
                )
                ic(
                    dataultimos["success"]["webHomeView"]["groups"][groupnumber][
                        "titles"
                    ][titlenumber]["chapterName"]
                )
                if (
                    str(
                        dataultimos["success"]["webHomeView"]["groups"][groupnumber][
                            "titles"
                        ][titlenumber]["chapterName"]
                    ).replace("#", "")
                    == "ex"
                ):
                    ic("capitulo especial")
                    separado = (
                        str(
                            mangasespeciales(
                                str(
                                    dataultimos["success"]["webHomeView"]["groups"][
                                        groupnumber
                                    ]["titles"][titlenumber]["chapterId"]
                                )
                            )
                        )
                        .replace("#", "")
                        .split(".")
                    )
                    numeroflotante = "{:0>4}".format(separado[0]) + "." + separado[1]
                    mangasnormales(
                        str(
                            dataultimos["success"]["webHomeView"]["groups"][
                                groupnumber
                            ]["titles"][titlenumber]["chapterId"]
                        ),
                        numeroflotante,
                        history,
                        mangas[
                            mapeo[
                                str(
                                    dataultimos["success"]["webHomeView"]["groups"][
                                        groupnumber
                                    ]["titles"][titlenumber]["title"]["titleId"]
                                )
                            ]
                        ],
                        mensaj,
                        mensaj2,
                    )
                elif "," in str(
                    dataultimos["success"]["webHomeView"]["groups"][groupnumber][
                        "titles"
                    ][titlenumber]["chapterName"]
                ):
                    mensaj2.append(
                        "El manga "
                        + mangas[
                            mapeo[
                                str(
                                    dataultimos["success"]["webHomeView"]["groups"][
                                        groupnumber
                                    ]["titles"][titlenumber]["title"]["titleId"]
                                )
                            ]
                        ]["Series"]
                        + " tiene los capitulos dobles "
                        + str(
                            dataultimos["success"]["webHomeView"]["groups"][
                                groupnumber
                            ]["titles"][titlenumber]["chapterName"]
                        )
                    )
                else:
                    ic(
                        str(
                            dataultimos["success"]["webHomeView"]["groups"][
                                groupnumber
                            ]["titles"][titlenumber]["chapterName"]
                        ).replace("#", "")
                    )
                    mangasnormales(
                        str(
                            dataultimos["success"]["webHomeView"]["groups"][
                                groupnumber
                            ]["titles"][titlenumber]["chapterId"]
                        ),
                        "{:0>4}".format(
                            str(
                                dataultimos["success"]["webHomeView"]["groups"][
                                    groupnumber
                                ]["titles"][titlenumber]["chapterName"]
                            ).replace("#", "")
                        ),
                        history,
                        mangas[
                            mapeo[
                                str(
                                    dataultimos["success"]["webHomeView"]["groups"][
                                        groupnumber
                                    ]["titles"][titlenumber]["title"]["titleId"]
                                )
                            ]
                        ],
                        mensaj,
                        mensaj2,
                    )
    with open(rutahistorial, "w") as outfile:
        json.dump(history, outfile)


def capitulossueltos(mensaj, mensaj2):
    capitulossueltos = "/opt/tachiyomimangaexporter/mangapluscapitulosueltos.json"
    if os.path.exists(capitulossueltos):
        with open(capitulossueltos) as json_file:
            chapters = json.load(json_file)

        with open("/opt/tachiyomimangaexporter/history.json") as json_file3:
            history = json.load(json_file3)

        deletefolder = "Error while deleting directory"
        tdescargas = "/media/cristian/Datos/Comics/Descargas"
        for chapter in chapters:

            historeturn = organizar.historial(history, chapter["number"], chapter)
            if historeturn == True and downloadchapter(
                tdescargas, chapter["chapterid"], chapter["name"], chapter["number"]
            ):
                update = False
                cbz = (
                    str(chapter["destino"])
                    + "/"
                    + str(chapter["name"])
                    + str(chapter["number"])
                    + ".cbz"
                )
                organizar.newinhistory(
                    chapter,
                    tdescargas + "/" + str(chapter["name"]) + str(chapter["number"]),
                    str(chapter["number"]),
                    deletefolder,
                    cbz,
                    update,
                    mensaj2,
                    mensaj,
                )
            if historeturn == "update" and downloadchapter(
                tdescargas, chapter["number"], chapter["name"], chapter["number"]
            ):
                cbz = (
                    str(chapter["destino"])
                    + "/"
                    + str(chapter["name"])
                    + str(chapter["number"])
                    + ".cbz"
                )
                update = True
                organizar.updatebook(chapter, tdescargas + "/" + str(chapter["name"]) + str(chapter["number"]), str(chapter["number"]), deletefolder, cbz, update, mensaj2, mensaj)
                history[chapter,].update({str(chapter["number"]): str(chapter["provider"])})
                
        os.remove(capitulossueltos)


def mangasnormales(chapterid, chapternumber, history, dic, mensaj, mensaj2):
    deletefolder = "Error while deleting directory"
    tdescargas = "/media/cristian/Datos/Comics/Descargas"
    historeturn = organizar.historial(history, chapternumber, dic)
    if historeturn == True and downloadchapter(
        tdescargas, chapterid, dic["name"], chapternumber
    ):
        update = False
        cbz = dic["destino"] + "/" + dic["name"] + chapternumber + ".cbz"
        organizar.newinhistory(
            dic,
            tdescargas + "/" + dic["name"] + chapternumber,
            chapternumber,
            deletefolder,
            cbz,
            update,
            mensaj2,
            mensaj,
        )
    if historeturn == "update" and downloadchapter(
        tdescargas, chapterid, dic["name"], chapternumber
    ):
        cbz = dic["destino"] + "/" + dic["name"] + chapternumber + ".cbz"
        ic(cbz)
        ic("se actualiza un manga")
        update = True
        organizar.updatebook(dic, tdescargas + "/" + dic["name"] + chapternumber, chapternumber, deletefolder, cbz, update, mensaj2, mensaj)
        history[dic["Series"]].update({chapternumber: dic["provider"]})
        


def mangasespeciales(chapterid):
    url = (
        api_url
        + "manga_viewer?chapter_id="
        + chapterid
        + "&split=no&img_quality=super_high&format=json"
    )
    responsechapter = requests.get(url, headers=headers)
    datachapter = responsechapter.json()
    for idx, val in enumerate(datachapter["success"]["mangaViewer"]["chapters"]):
        # ic(val["chapterId"], chapterid)
        if str(val["chapterId"]) == chapterid:
            ic(idx, val)
            ic(
                "Es un capitulo especial y el inidice va a ser: "
                + datachapter["success"]["mangaViewer"]["chapters"][int(idx) - 1][
                    "name"
                ]
            )
            negaindice = int(idx)

    if len(datachapter["success"]["mangaViewer"]["chapters"]) <= 1:
        return (
            datachapter["success"]["mangaViewer"]["chapters"][negaindice]["name"] + ".1"
        )
    contador = 0
    while (
        str(
            datachapter["success"]["mangaViewer"]["chapters"][negaindice]["name"]
        ).replace("#", "")
        == "ex"
    ):
        negaindice -= 1
        contador += 1
    ic(
        "El indice negativo del capitulo es: "
        + str(negaindice)
        + " y el contador es: "
        + str(contador)
    )
    ic(
        "Capitulo devuelto es: "
        + datachapter["success"]["mangaViewer"]["chapters"][negaindice]["name"]
        + "."
        + str(contador)
    )
    return (
        datachapter["success"]["mangaViewer"]["chapters"][negaindice]["name"]
        + "."
        + str(contador)
    )


def mangascompletos(mensaj, mensaj2):
    with open("/opt/tachiyomimangaexporter/mangaplusmapper.json") as json_file:
        mapeo = json.load(json_file)
    with open("/opt/tachiyomimangaexporter/mangas.json") as json_file2:
        mangas = json.load(json_file2)
    with open(rutahistorial) as json_file3:
        history = json.load(json_file3)

    for key in mapeo.keys():
        if mangas[mapeo[key]]["Series"] not in history:
            url = (
                api_url
                + "title_detail?title_id="
                + str(mangas[mapeo[key]]["mangaid"])
                + "&format=json"
            )
            responsetodos = requests.get(url, headers=headers)
            datatodos = responsetodos.json()
            ic(
                mangas[mapeo[key]]["Series"]
                + ": No esta en History y se va descargar completo"
            )
            if "firstChapterList" in datatodos["success"]["titleDetailView"]:
                for chapters in datatodos["success"]["titleDetailView"][
                    "firstChapterList"
                ]:
                    organizar.folderinit(mangas[mapeo[key]])
                    ic("First Chapters " + chapters["name"])
                    if str(chapters["name"]).replace("#", "") == "ex":
                        separado = (
                            str(mangasespeciales(str(chapters["chapterId"])))
                            .replace("#", "")
                            .split(".")
                        )
                        numeroflotante = (
                            "{:0>4}".format(separado[0]) + "." + separado[1]
                        )
                        mangasnormales(
                            str(chapters["chapterId"]),
                            numeroflotante,
                            history,
                            mangas[mapeo[key]],
                            mensaj,
                            mensaj2,
                        )
                    elif "," in str(chapters["name"]):
                        mensaj2.append(
                            "El manga "
                            + mangas[mapeo[key]]["Series"]
                            + " tiene los capitulos dobles "
                            + str(chapters["name"])
                        )
                    else:
                        ic(str(chapters["name"]).replace("#", ""))
                        mangasnormales(
                            str(chapters["chapterId"]),
                            "{:0>4}".format(str(chapters["name"]).replace("#", "")),
                            history,
                            mangas[mapeo[key]],
                            mensaj,
                            mensaj2,
                        )
            if "lastChapterList" in datatodos["success"]["titleDetailView"]:
                for chapters in datatodos["success"]["titleDetailView"][
                    "lastChapterList"
                ]:
                    organizar.folderinit(mangas[mapeo[key]])
                    ic("Last Chapters " + chapters["name"])
                    if str(chapters["name"]).replace("#", "") == "ex":
                        separado = (
                            str(mangasespeciales(str(chapters["chapterId"])))
                            .replace("#", "")
                            .split(".")
                        )
                        numeroflotante = (
                            "{:0>4}".format(separado[0]) + "." + separado[1]
                        )
                        mangasnormales(
                            str(chapters["chapterId"]),
                            numeroflotante,
                            history,
                            mangas[mapeo[key]],
                            mensaj,
                            mensaj2,
                        )
                    elif "," in str(chapters["name"]):
                        mensaj2.append(
                            "El manga "
                            + mangas[mapeo[key]]["Series"]
                            + " tiene los capitulos dobles "
                            + str(chapters["name"])
                        )
                    else:
                        ic(str(chapters["name"]).replace("#", ""))
                        mangasnormales(
                            str(chapters["chapterId"]),
                            "{:0>4}".format(str(chapters["name"]).replace("#", "")),
                            history,
                            mangas[mapeo[key]],
                            mensaj,
                            mensaj2,
                        )
    ic("Se va a actualizar el Historial")
    with open(rutahistorial, "w") as outfile:
        json.dump(history, outfile)


def mangaplusmain():
    mensaj = []
    mensaj2 = []
    with open("/opt/tachiyomimangaexporter/secrets.json") as json_file1:
        secrets = json.load(json_file1)
    nuevosmangas()
    mangascompletos(mensaj, mensaj2)
    capitulossueltos(mensaj, mensaj2)
    ultimosmangas(mensaj, mensaj2)
    # mangaplusmapper()
    organizar.scankomgalibrary(
        mensaj, mensaj2, secrets["komgauser"], secrets["komgapass"]
    )
    organizar.send(mensaj, mensaj2)
