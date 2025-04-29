import ninemanga.loader
import requests
from functions import sendmsg, filterchapters, historial, organizer
from bs4 import BeautifulSoup
# import cfscrape
import json
from icecream import ic
import os
from PIL import Image
manga_url = ''

global scraper


def flaresolverr(url_manga):
    url = "http://royflix.net:20080/v1"
    headers = {"Content-Type": "application/json"}

    scraper = {
        "cmd": "request.get",
        "url": url_manga,
        "maxTimeout": 60000
    }
    urlmanga = requests.post(url, headers=headers, json=scraper)
    json_data = json.loads(urlmanga.text)
    return json_data


def downloadchapter(href, dic, chapternumber):
    ic(f'Se va a descargar el capitulo {chapternumber} de: {dic["Series"]} - {dic["provider"]}')
    dfolder = f'{ninemanga.loader.tdescargas}/{dic["Series"]} - {dic["provider"]} {chapternumber}/'
    if not os.path.exists(dfolder):
        os.makedirs(dfolder)
    capitulos = flaresolverr(href)
    intentos = 0
    while 'solution' not in capitulos and intentos < 10:
        capitulos = flaresolverr(href)
        intentos += 1
    chaptersoup = BeautifulSoup(capitulos["solution"]['response'], 'lxml')
    # ic(chaptersoup)
    chapterpagesdiv = chaptersoup.find('div', class_="changepage")
    # ic(chapterpagesdiv)
    contador = 0
    try:
        for option in chapterpagesdiv.find_all("option"):
            chapterimagesurl = dic['web_url'] + option['value'] + ninemanga.loader.waring
            capituloimageurl = flaresolverr(chapterimagesurl)
            while 'solution' not in capituloimageurl:
                capitulos = flaresolverr(chapterimagesurl)
            chapterimagessoup = BeautifulSoup(flaresolverr(chapterimagesurl)["solution"]['response'], 'lxml')
            for img in chapterimagessoup.find_all('img', class_='manga_pic'):
                imagenumber = int(img.attrs["i"]) + contador
                try:
                    im = Image.open(requests.get(img.attrs["src"], stream=True).raw).convert("RGB")
                    ic(f'Descargando la pagina {imagenumber}')
                    imageroute = (dfolder + "{:0>3}".format(str(imagenumber)) + ".jpg")
                    im.save(imageroute, "jpeg")
                except OSError:
                    try:
                        newimage = str(img.attrs["src"]).replace('taadd.com', 'ourclub.cc')
                        im = Image.open(requests.get(newimage, stream=True).raw).convert("RGB")
                        ic(f'Descargando la pagina {imagenumber}')
                        imageroute = (dfolder + "{:0>3}".format(str(imagenumber)) + ".jpg")
                        im.save(imageroute, "jpeg")
                    except OSError:
                        ic(f'La imagen {imagenumber} esta truncada o no se ha descargado bien')
                        ninemanga.loader.mensaj2.append(f'La imagen {imagenumber} de {dic["Series"]} - {dic["provider"]} - {chapternumber} esta truncada o no se ha descargado bien')
                        sendmsg.sendnewmsg('fallo', ninemanga.loader.mensaj2, 'Fallo Download')
                        # sendmsgtelegram.sendmsg(ninemanga.loader.secrets["token"], ninemanga.loader.secrets["chatid"], ninemanga.loader.mensaj2)
                        # sendmsgdiscord.sendmsg(ninemanga.loader.secrets["disdcordwebhookfallo"], ninemanga.loader.mensaj2)
                        ninemanga.loader.mensaj2 = []
            contador += 10
        ic('Se ha Descargado todas la paginas')
        return True
    except Exception as e:
        ic(e)
        sendmsg.sendnewmsg('fallo', ninemanga.loader.mensaj2, f'Fallo Download {dic["Series"]}')
        return False


def wrongchaptername(enlace, manga):
    if manga_url in ninemanga.loader.ninemangaurls:
        if enlace.attrs['href'] in ninemanga.loader.ninemangaurls[manga_url]:
            if ninemanga.loader.ninemangaurls[manga_url][enlace.attrs['href']]['number'] == '' or ninemanga.loader.ninemangaurls[manga_url][enlace.attrs['href']]['status'] != 'new':
                return '', False

            ninemanga.loader.ninemangaurls[manga_url][enlace.attrs['href']]['status'] = 'downloaded'
            historyreturn = historial.historial(ninemanga.loader.history, ninemanga.loader.ninemangaurls[manga_url][enlace.attrs['href']]['number'], ninemanga.loader.mangas[manga], ninemanga.loader.komgabooksid)
            ic(f"Se va a descargar el cap {ninemanga.loader.ninemangaurls[manga_url][enlace.attrs['href']]['number']} por que es un cap especial ya modificado en el json")
            return ninemanga.loader.ninemangaurls[manga_url][enlace.attrs['href']]['number'], historyreturn
        else:
            ninemanga.loader.ninemangaurls[manga_url][enlace.attrs['href']] = {
                "name": enlace.attrs['title'],
                "number": "",
                "status": "new",
                "series": f"{ninemanga.loader.mangas[manga]['Series']} - {ninemanga.loader.mangas[manga]['provider']}"
            }
            ic(f"El manga {ninemanga.loader.mangas[manga]['Series']} - {ninemanga.loader.mangas[manga]['provider']} tienen un capitulo especial que hay modificar: {enlace.attrs['title']}")
            ninemanga.loader.mensaj2.append(f"El manga {ninemanga.loader.mangas[manga]['Series']} - {ninemanga.loader.mangas[manga]['provider']} tienen un capitulo especial que hay modificar: {enlace.attrs['title']} \n\n")
            sendmsg.sendnewmsg('fallo', ninemanga.loader.mensaj2, 'Capitulo Especial')
            # sendmsgtelegram.sendmsg(ninemanga.loader.secrets["token"], ninemanga.loader.secrets["chatid"], ninemanga.loader.mensaj2)
            # sendmsgdiscord.sendmsg(ninemanga.loader.secrets["disdcordwebhookfallo"], ninemanga.loader.mensaj2)
            ninemanga.loader.mensaj2 = []
            return '', False
    else:
        ninemanga.loader.ninemangaurls[manga_url] = {}
        ninemanga.loader.ninemangaurls[manga_url][enlace.attrs['href']] = {
            "name": enlace.attrs['title'],
            "number": "",
            "status": "new",
            "series": f"{ninemanga.loader.mangas[manga]['Series']} - {ninemanga.loader.mangas[manga]['provider']}"
        }
        ic(f"El manga {ninemanga.loader.mangas[manga]['Series']} - {ninemanga.loader.mangas[manga]['provider']} tienen un capitulo especial que hay modificar: {enlace.attrs['title']}")
        ninemanga.loader.mensaj2.append(f"El manga {ninemanga.loader.mangas[manga]['Series']} - {ninemanga.loader.mangas[manga]['provider']} tienen un capitulo especial que hay modificar: {enlace.attrs['title']} \n\n")
        sendmsg.sendnewmsg('fallo', ninemanga.loader.mensaj2, 'Capitulo Especial')
        # sendmsgtelegram.sendmsg(ninemanga.loader.secrets["token"], ninemanga.loader.secrets["chatid"], ninemanga.loader.mensaj2)
        # sendmsgdiscord.sendmsg(ninemanga.loader.secrets["disdcordwebhookfallo"], ninemanga.loader.mensaj2)
        ninemanga.loader.mensaj2 = []
        return '', False


def checkchapter(enlace, manga):
    chapternumber, filtercorrect = filterchapters.filterchapter(
        enlace.attrs['title'], ninemanga.loader.mangas[manga])
    if filtercorrect:
        historyreturn = historial.historial(
            ninemanga.loader.history, chapternumber, ninemanga.loader.mangas[manga], ninemanga.loader.komgabooksid)
    else:
        chapternumber, historyreturn = wrongchaptername(enlace, manga)
    ic(manga, chapternumber, historyreturn)
    if historyreturn and downloadchapter(enlace.attrs['href'], ninemanga.loader.mangas[manga], chapternumber):
        ic('Es un manga nuevo')
        update = False
        cbz = ninemanga.loader.mangas[manga]["destino"] + "/" + \
            ninemanga.loader.mangas[manga]["name"] + chapternumber + ".cbz"
        organizer.newinhistory(
            ninemanga.loader.mangas[manga], f'{ninemanga.loader.tdescargas}/{ninemanga.loader.mangas[manga]["Series"]} - {ninemanga.loader.mangas[manga]["provider"]} {chapternumber}/', chapternumber, ninemanga.loader.deletefolder, cbz, update, ninemanga.loader.mensaj2, ninemanga.loader.mensaj, ninemanga.loader.secrets)
        ninemanga.loader.save()

    if historyreturn == "update" and downloadchapter(enlace.attrs['href'], ninemanga.loader.mangas[manga], chapternumber):
        ic("Se actualiza un manga")
        cbz = ninemanga.loader.mangas[manga]["destino"] + "/" + \
            ninemanga.loader.mangas[manga]["name"] + chapternumber + ".cbz"

        update = True
        organizer.updatebook(
            ninemanga.loader.mangas[manga], f'{ninemanga.loader.tdescargas}/{ninemanga.loader.mangas[manga]["Series"]} - {ninemanga.loader.mangas[manga]["provider"]} {chapternumber}/', chapternumber, ninemanga.loader.deletefolder, cbz, update, ninemanga.loader.mensaj2, ninemanga.loader.mensaj, ninemanga.loader.secrets)

        ninemanga.loader.history[ninemanga.loader.mangas[manga]["Series"]].update(
            {chapternumber: ninemanga.loader.mangas[manga]["provider"]})
        ninemanga.loader.save()


def main():
    global manga_url

    lista = [[ninemanga.loader.mangas[manga]['Series'], manga] for manga in ninemanga.loader.mangas]
    newmangas = {key[1]: ninemanga.loader.mangas[key[1]] for key in sorted(lista, key=lambda x: x[0])}
    ninemangalist = [key for key in newmangas if newmangas[key]
                     ['provider'] in ['NineMangaEs (ES)', 'NineMangaEn (EN)']]
    for manga in ninemangalist:

        waring = ninemanga.loader.mangas[manga]["manga_url"] + ninemanga.loader.waring if str(
            ninemanga.loader.mangas[manga]["manga_url"]).split('?')[-1] != ninemanga.loader.waring else ninemanga.loader.mangas[manga]["manga_url"]

        manga_url = ninemanga.loader.mangas[manga]["web_url"] + waring
        ic(f'Revisando manga {ninemanga.loader.mangas[manga]["Series"]} - {ninemanga.loader.mangas[manga]["provider"]} - {manga_url}')
        # ic(urlmanga.text)
        # with open(f'/home/cristian/Github/mamicorganizerr-legacy/app/ninemanga/response/{ninemanga.loader.mangas[manga]["Series"]}.json', 'w', encoding='utf-8') as f:
        #     json.dump(json_data, f, indent=4, ensure_ascii=False)
        # thejson = flaresolverr(manga_url)
        # ic(thejson['response'])

        capitulos = flaresolverr(manga_url)
        intentos = 0
        while 'solution' not in capitulos and intentos < 10:
            capitulos = flaresolverr(manga_url)
            intentos += 1
        chapterlistsoup = BeautifulSoup(capitulos["solution"]['response'], 'lxml')
        chapterlistenlaces = chapterlistsoup.find_all(
            'a', class_="chapter_list_a")
        for enlace in chapterlistenlaces:
            checkchapter(enlace, manga)
            ic(enlace, manga)

    organizer.scankomgalibrary(
        ninemanga.loader.mensaj, ninemanga.loader.mensaj2, ninemanga.loader.secrets["komgauser"], ninemanga.loader.secrets["komgapass"], ninemanga.loader.secrets
    )
    # organizer.send(ninemanga.loader.mensaj, ninemanga.loader.mensaj2)
