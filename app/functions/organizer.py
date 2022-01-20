import os
import requests
from requests.auth import HTTPBasicAuth
import re
import shutil
import xml.etree.cElementTree as ET
from os.path import basename
from zipfile import ZipFile
import telegram
import time
import glob
import json
from discord import Webhook, RequestsWebhookAdapter
from icecream import ic
from urllib import response
import urllib


def send(msg, msg2):
    """
    Send a message to a telegram user or group specified on chatId
    chat_id must be a number!
    """

    if msg:
        enviarmensaje(msg, "Siguientes Comics/Mangas se han descargado:\n\n", False)

    if msg2:
        enviarmensaje(msg2, "Siguientes Comics/Mangas han fallado:\n\n", True)


def enviarmensaje(arg0, arg1, arg2):
    with open("/opt/tachiyomimangaexporter/secrets.json") as json_file2:
        secrets = json.load(json_file2)
    arg0.sort()
    telegrammnsj = arg1
    discordmnsj = arg1
    if arg2:
        urlwebhook = secrets["disdcordwebhookfallo"]
    else:
        urlwebhook = secrets["disdcordwebhook"]

    for string in arg0:
        telegramlen = len(telegrammnsj) + len(string)
        discordlen = len(discordmnsj) + len(string)
        if telegramlen < 4096:
            telegrammnsj += string
        else:
            time.sleep(2)
            bot = telegram.Bot(token=secrets["token"])
            bot.sendMessage(chat_id=secrets["chatid"], text=telegrammnsj)
            telegrammnsj = string
        if discordlen < 2000:
            discordmnsj += string
        else:
            webhook = Webhook.from_url(
                urlwebhook,
                adapter=RequestsWebhookAdapter(),
            )
            webhook.send(discordmnsj)
            discordmnsj = string
    bot = telegram.Bot(token=secrets["token"])
    bot.sendMessage(chat_id=secrets["chatid"], text=telegrammnsj)
    webhook = Webhook.from_url(
        urlwebhook,
        adapter=RequestsWebhookAdapter(),
    )
    webhook.send(discordmnsj)


def isfloat(x):
    try:
        float(x)
    except ValueError:
        return False
    else:
        return True


def isint(x):
    try:
        a = float(x)
        b = int(a)
    except ValueError:
        return False
    else:
        return a == b


def generatexml(dic, finalpath, numero):
    root = ET.Element(
        "ComicInfo",
        **{
            "xmlns:xsd": "http://www.w3.org/2001/XMLSchema",
            "xmlns:xsi": "http://www.w3.org/2001/XMLSchema-instance",
        }
    )

    ET.SubElement(
        root,
        "Series",
    ).text = dic["Series"]
    ET.SubElement(
        root,
        "Number",
    ).text = numero
    ET.SubElement(
        root,
        "Volume",
    ).text = dic["Volume"]
    ET.SubElement(
        root,
        "Publisher",
    ).text = dic["Publisher"]

    tree = ET.ElementTree(root)
    filename = finalpath + "/ComicInfo.xml"
    tree.write(filename, encoding="utf-8", xml_declaration=True)


def historial(history, issue, dic):
    if dic["Series"] in history:
        if issue in history[dic["Series"]]:
            if dic["provider"] == history[dic["Series"]][issue]:
                return False
            if dic["funcion"] == history[dic["Series"]][issue]:
                return False
            history[dic["Series"]].pop(issue, None)
            with open("/opt/tachiyomimangaexporter/komgabooksid.json") as komgabooksid_file:
                komgabooksid = json.load(komgabooksid_file)
            komgabooksid[dic["Series"]].pop(issue, None)
            return "update"
        else:
            history[dic["Series"]].update({issue: dic["provider"]})
            return True
    else:
        history[dic["Series"]] = {issue: dic["provider"]}
        return True


def postermangaplus(manga):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36"
    }
    url = manga["portrait"]
    image = requests.get(url, headers=headers)
    imagesave = str(manga["destino"] + "/poster.jpg")
    with open(imagesave, "wb") as f:
        f.write(image.content)


def posterm(manga):
    url = "https://kitsu.io/api/edge/manga?filter[slug]=" + manga["slug"]
    response = requests.get(url)
    data = response.json()
    image = requests.get(data["data"][0]["attributes"]["posterImage"]["large"])
    imagesave = str(manga["destino"] + "/poster.jpg")
    with open(imagesave, "wb") as f:
        f.write(image.content)


def posterc(manga):
    print(manga["Series"])
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36"
    }
    url = (
        "https://comicvine.gamespot.com/api/volume/"
        + manga["slug"]
        + "/?api_key=dcb22bb374f04e7217eaca81f2fcfffbe5062e42&format=json"
    )
    response = requests.get(url, headers=headers)
    print(url, response)
    data = response.json()
    image = requests.get(data["results"]["image"]["super_url"])
    imagesave = str(manga["destino"] + "/poster.jpg")
    with open(imagesave, "wb") as f:
        f.write(image.content)


def folderinit(dic):
    if not os.path.exists(dic["destino"]):
        os.makedirs(dic["destino"])
    poster = str(dic["destino"]) + "/poster.jpg"
    if dic["slug"] != "undefined" and not os.path.exists(poster):
        if dic["Publisher"] in ["DC Comics", "Marvel"]:
            posterc(dic)
        else:
            posterm(dic)
    if "portrait" in dic and not os.path.exists(dic["destino"] + "/poster.jpg"):
        postermangaplus(dic)


def cyanideorganizer(dic, finalpath, mensaj, mensaj2, history, fecha):
    deletefolder = "Error while deleting directory"
    historeturn = historial(history, fecha, dic)
    if historeturn == True:
        generatexml(dic, finalpath, fecha)
        cbz = dic["destino"] + "/" + dic["name"] + fecha + ".cbz"
        archivos = os.listdir(finalpath)
        archivos.sort()
        zipobje = ZipFile(cbz, "w")
        for archivos2 in archivos:
            finalpath2 = finalpath + "/" + archivos2
            zipobje.write(finalpath2, basename(archivos2))
        zipobje.close()
        try:
            shutil.rmtree(finalpath)
        except OSError:
            print(deletefolder)

        mensaj.append(dic["name"] + fecha + "\n\n")
    if historeturn == False:
        try:
            shutil.rmtree(finalpath)
        except OSError:
            print(deletefolder)
        mensaj2.append(finalpath + " El Issue existe con el proveedor correcto \n\n")


def issueorganizer(dic, finalpath, mensaj, mensaj2, history, numero, cap):
    deletefolder = "Error while deleting directory"
    if isint(numero) or isfloat(numero):
        if isint(numero):
            if '.' not in numero:
                issue = "{:0>4}".format(numero)
            else:
                issue = "{:0>4}".format(str(numero).split('.')[0])
        elif isfloat(numero):
            separado = numero.split(".")
            if separado[1] != '0' or separado[1] != '00':
                issue = "{:0>4}".format(separado[0]) + '.' + separado[1]
            else:
                issue = "{:0>4}".format(separado[0])
        historeturn = historial(history, issue, dic)
        if historeturn == True:
            cbz = dic["destino"] + "/" + dic["name"] + issue + ".cbz"
            update = False
            newinhistory(
                dic, finalpath, issue, deletefolder, cbz, update, mensaj2, mensaj
            )
        if historeturn == False:
            historycorrect(finalpath, deletefolder, mensaj2)

        if historeturn == "update":
            cbz = (
                "/media/cristian/Datos/Comics/Tachiyomi/Updates/"
                + dic["name"]
                + issue
                + ".cbz"
            )
            update = True
            newinhistory(
                dic, finalpath, issue, deletefolder, cbz, update, mensaj2, mensaj
            )
    else:
        try:
            shutil.move(finalpath, "/media/cristian/Datos/Comics/Fallo/" + cap)
        except OSError:
            print(deletefolder)
        try:
            shutil.rmtree(finalpath)
        except OSError:
            print(deletefolder)

        mensaj2.append(finalpath + " Patron encontrado es: " + numero + "\n\n")


def newinhistory(dic, finalpath, issue, deletefolder, cbz, update, mensaj2, mensaj):
    generatexml(dic, finalpath, issue)
    if update == True:
        eliminado = dic["destino"] + "/" + dic["name"] + issue + ".cbz"
    archivos = os.listdir(finalpath)
    archivos.sort()
    zipobje = ZipFile(cbz, "w")
    for archivos2 in archivos:
        finalpath2 = finalpath + "/" + archivos2
        zipobje.write(finalpath2, basename(archivos2))
    zipobje.close()
    try:
        shutil.rmtree(finalpath)
    except OSError:
        print(deletefolder)
    if update == True:
        try:
            os.remove(eliminado)
        except OSError:
            print(deletefolder)
        mensaj2.append(
            dic["name"] + issue + " eliminado para su futura actualizacion \n\n"
        )
    else:
        mensaj.append(dic["name"] + issue + "\n\n")


def historycorrect(finalpath, deletefolder, mensaj2):
    try:
        shutil.rmtree(finalpath)
    except OSError:
        print(deletefolder)
    mensaj2.append(finalpath + " El Issue existe con el proveedor correcto \n\n")


def organizer(elemento, dic, finalpath, mensaj, mensaj2, history):
    folderinit(dic)
    tilde = False
    tags = [
        "ep",
        "ch",
        "chapter",
        "chapterr",
        "chap",
        "episodio",
        "capitulo",
        "num",
        "issue",
        "generations",
    ]

    numero = ""
    fecha = ""
    cadena = (
        elemento[1]
        .lower()
        .replace("ch.", "ch ")
        .replace(":", " ")
        .replace(u"núm.", "num ")
        .replace(u"ó", "o")
        .replace(u"á", "a")
        .replace(u"́é", "e")
        .replace(u"í", "i")
        .replace(u"ú", "u")
        .replace(u"ñ", "n")
        .replace(u"é", "e")
        .replace(u"“", "")
        .replace(u"”", "")
        .replace(u"«", "")
        .replace(u"»", "")
        .replace(u"ô", "o")
        .replace(u"â", "a")
        .replace(".hu", "")
        .replace(".lr", "")
        .replace("shueisha_", "")
        .replace("mangakakalot.com_", "")
        .replace("readmanganato.com_", "")
        .replace("_tmp", "tmp")
        .replace("_", " ")
    )
    # ic(cadena)
    palabra = 0
    primero = False
    continuar = True
    while continuar:
        if palabra == 0:
            if re.findall("^#", cadena.split()[palabra]):
                numero = cadena.split()[palabra].replace("#", "")
                primero = True
                tilde = True
            if re.findall(
                "[0-9][0-9][0-9][0-9]\.[0-9][0-9]\.[0-9][0-9]", cadena.split()[palabra]
            ):
                fecha = cadena.split()[palabra]
                primero = True
                tilde = True
            if cadena.split()[palabra] in tags:
                if re.findall("^\.", cadena.split()[palabra + 1]) or re.findall(
                    "\.$", cadena.split()[palabra + 1]
                ):
                    numero = cadena.split()[palabra + 1].replace(".", "")
                    primero = True
                else:
                    numero = cadena.split()[palabra + 1]
                    primero = True
                tilde = True

        else:
            cadena = cadena.replace("#", "")
            if cadena.split()[palabra] in tags:
                if re.findall("^\.", cadena.split()[palabra + 1]) or re.findall(
                    "\.$", cadena.split()[palabra + 1]
                ):
                    numero = cadena.split()[palabra + 1].replace(".", "")
                    primero = True
                else:
                    numero = cadena.split()[palabra + 1]
                    primero = True
                tilde = True
        palabra += 1
        if primero:
            continuar = False
        if palabra >= len(cadena.split()):
            continuar = False
    if not tilde:
        titulo = (
            elemento[0]
            .replace(u"·", "")
            .replace(u"ô", "o")
            .replace(":", " ")
            .replace("-", " ")
            .replace(".", " ")
        )
        cadena = (
            cadena.lower()
            .replace(elemento[0].lower().replace(u"·", "").replace(u"ô", "o"), "")
            .replace(":", " ")
            .replace("-", " ")
        )
        for words in range(len(titulo.split())):
            cadena = cadena.replace(titulo.split()[words].lower(), "")
        if re.findall(
            "^vol\.",
            cadena.lower()
            .replace(elemento[0].lower().replace(u"·", ""), "")
            .replace(" ", ""),
        ) or re.findall(
            "^vol",
            cadena.lower()
            .replace(elemento[0].lower().replace(u"·", ""), "")
            .replace(" ", ""),
        ):
            cadena = cadena.replace("vol.", "").replace("vol", "")
            # print(cadena.lower().replace(elemento[0].lower().replace(u'·',''),'').replace(' ', '').replace('vol.', ''))
        elif re.findall(
            "^\.",
            cadena.lower()
            .replace(elemento[0].lower().replace(u"·", ""), "")
            .replace(" ", ""),
        ) or re.findall(
            "\.$",
            cadena.lower()
            .replace(elemento[0].lower().replace(u"·", ""), "")
            .replace(" ", ""),
        ):
            cadena = cadena.replace(".", "").replace(" ", "")
            # print(cadena.lower().replace(elemento[0].lower().replace(u'·',''),'').replace(' ', '').replace('.', ''))

        cadena = cadena.replace(" ", "")
        numero = cadena
    # ic(numero)
    if numero != "":
        issueorganizer(dic, finalpath, mensaj, mensaj2, history, numero, elemento[1])

    if fecha != "":
        cyanideorganizer(dic, finalpath, mensaj, mensaj2, history, fecha)
    tilde = False


def issueupdate(secrets, mangas):
    with open("/opt/tachiyomimangaexporter/history.json") as json_file:
        history = json.load(json_file)
    folder = "/media/cristian/Datos/Comics/Tachiyomi/Updates"
    mensaje = []
    mensaje2 = ""
    if len(os.listdir(folder)) != 0:
        updates = glob.glob(folder + "/**/*.[cC][bB][zZ]", recursive=True)
        for issues in updates:
            fichero = os.path.split(issues)
            filename = os.path.splitext(fichero[1])
            issue = filename[0].split("#")
            name = issue[0] + "#"
            for key in mangas:
                if mangas[key]["name"] == name:
                    historial(history, issue[-1], mangas[key])
                    destino = str(mangas[key]["destino"]) + "/" + str(fichero[1])
                    namefile = str(fichero[0]) + "/" + str(fichero[1])
                    shutil.move(namefile, destino)
                    mensaje.append(str(mangas[key]["name"]) + str(issue[-1]) + "\n\n")
                    break
        with open("/opt/tachiyomimangaexporter/history.json", "w") as outfile:
            json.dump(history, outfile)
        send(mensaje, mensaje2)
        time.sleep(2)


def scankomgalibrary(mensaj, mensaj2, user, password):
    print(mensaj, mensaj2)
    if mensaj != [] or mensaj2 != []:
        print("paso por aqui")
        response = requests.post(
            "https://komga.loyhouse.net/api/v1/libraries/02G13VGFYC532/scan",
            data={"accept": "*/*"},
            auth=HTTPBasicAuth(user, password),
        )
        if response.status_code != 202:
            mensaj2.append(str(response))


def komgabookid():
    configpath = "/opt/tachiyomimangaexporter/"

    komga = "komgabooksid.json"

    with open(configpath + "mangas.json") as mangas_file:
        mangas = json.load(mangas_file)

    with open(configpath + "history.json") as history_file:
        history = json.load(history_file)

    with open(configpath + "secrets.json") as secrets_file:
        secrets = json.load(secrets_file)

    with open(configpath + komga) as komgabooksid_file:
        komgabooksid = json.load(komgabooksid_file)


    intermedia = {mangas[manga]["Series"]: manga for manga in mangas}

    for serie in history:
        for capitulo in history[serie]:
            if serie not in komgabooksid:
                nombre = mangas[intermedia[serie]]["name"] + capitulo
                # ic(nombre)
                url = urllib.parse.quote_plus(nombre)
                ic(url)
                query = (
                    "https://komga.loyhouse.net/api/v1/books?search=%22"
                    + url
                    + "%22&library_id=02G13VGFYC532"
                )
                reponse = requests.get(
                    query,
                    data={"accept": "*/*"},
                    auth=HTTPBasicAuth(secrets["komgauser"], secrets["komgapass"]),
                )
                ic(reponse.json())
                book = reponse.json()
                komgabooksid[mangas[intermedia[serie]]["Series"]] = {
                            capitulo: book["content"][0]["id"]
                        }

            elif capitulo not in komgabooksid[serie]:
                    nombre = mangas[intermedia[serie]]["name"] + capitulo
                    # ic(nombre)
                    url = urllib.parse.quote_plus(nombre)
                    ic(url)
                    query = (
                        "https://komga.loyhouse.net/api/v1/books?search=%22"
                        + url
                        + "%22&library_id=02G13VGFYC532"
                    )
                    reponse = requests.get(
                        query,
                        data={"accept": "*/*"},
                        auth=HTTPBasicAuth(secrets["komgauser"], secrets["komgapass"]),
                    )
                    ic(reponse.json())
                    book = reponse.json()
                    
                    komgabooksid[mangas[intermedia[serie]]["Series"]].update(
                        {capitulo: book["content"][0]["id"]}
                    )
         

    with open(configpath + komga, "w") as outfile:
        json.dump(komgabooksid, outfile)