from fileinput import filename
import requests
import getcomicsinfo.loader as loader
from icecream import ic
import os
import shutil
import patoolib
import xml.etree.cElementTree as ET
import xmltodict
import glob
from zipfile import ZipFile
from os.path import basename
from getcomicsinfo.functions import historial, sendmsgdiscord, sendmsgtelegram, scankomgalibrary


def person_credit(dataissue, root):
    writer = []
    penciller = []
    inker = []
    colorist = []
    letterer = []
    editor = []
    cover_artist = []
    for person in dataissue["results"]["person_credits"]:
        if(person["role"] == "writer"):
            writer.append(person["name"])

        if(person["role"] == "penciller"):
            penciller.append(person["name"])

        if(person["role"] == "inker"):
            inker.append(person["name"])

        if(person["role"] == "colorist"):
            colorist.append(person["name"])

        if(person["role"] == "letterer"):
            letterer.append(person["name"])

        if(person["role"] == "editor"):
            editor.append(person["name"])

        if(person["role"] in ["cover_artist", "cover"]):
            cover_artist.append(person["name"])
    if writer:
        ET.SubElement(root, "Writer").text = ",".join(writer)
    if penciller:
        ET.SubElement(root, "Penciller").text = ",".join(penciller)
    if inker:
        ET.SubElement(root, "Inker").text = ",".join(inker)
    if colorist:
        ET.SubElement(root, "Colorist").text = ",".join(colorist)
    if letterer:
        ET.SubElement(root, "Letterer").text = ",".join(letterer)
    if editor:
        ET.SubElement(root, "Editor").text = ",".join(editor)
    if cover_artist:
        ET.SubElement(root, "CoverArtist").text = ",".join(cover_artist)


def getposter(my_dict, destino):
    web = my_dict["ComicInfo"]["Web"]
    issueid = web.split("/")[-2:][0]
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36"
    }
    url = (
        "https://comicvine.gamespot.com/api/issue/"
        + issueid
        + "/?api_key=dcb22bb374f04e7217eaca81f2fcfffbe5062e42&format=json"
    )
    responseissue = requests.get(url, headers=headers)
    dataissue = responseissue.json()
    url = (
        dataissue["results"]["volume"]["api_detail_url"]
        + "?api_key=dcb22bb374f04e7217eaca81f2fcfffbe5062e42&format=json"
    )
    responsevolume = requests.get(url, headers=headers)
    # print(url, response)
    datavolume = responsevolume.json()
    image = requests.get(datavolume["results"]["image"]["super_url"])
    imagesave = str(f"{destino}/poster.jpg")
    with open(imagesave, "wb") as f:
        f.write(image.content)


def treeelement(datavolume, dataissue, web):
    root = ET.Element(
        "ComicInfo",
        **{
            "xmlns:xsd": "http://www.w3.org/2001/XMLSchema",
            "xmlns:xsi": "http://www.w3.org/2001/XMLSchema-instance",
        }
    )
    if(dataissue["results"]["name"]):
        ET.SubElement(root, "Title").text = dataissue["results"]["name"]
    if(dataissue["results"]["volume"]["name"]):
        ET.SubElement(
            root, "Series").text = dataissue["results"]["volume"]["name"]
    if(dataissue["results"]["issue_number"]):
        ET.SubElement(
            root, "Number").text = "{:0>4}".format(dataissue["results"]["issue_number"])
    if(datavolume["results"]["start_year"]):
        ET.SubElement(
            root, "Volume").text = datavolume["results"]["start_year"]
    if(dataissue["results"]["description"]):
        ET.SubElement(
            root, "Summary").text = dataissue["results"]["description"]
    if(dataissue["results"]["store_date"]):
        ET.SubElement(
            root, "Year").text = dataissue["results"]["store_date"].split("-")[0]
        ET.SubElement(
            root, "Month").text = dataissue["results"]["store_date"].split("-")[1]
        ET.SubElement(
            root, "Day").text = dataissue["results"]["store_date"].split("-")[2]

    if dataissue["results"]["person_credits"]:
        person_credit(dataissue, root)

    if datavolume["results"]["publisher"]:
        ET.SubElement(
            root, "Publisher").text = datavolume["results"]["publisher"]["name"]
    ET.SubElement(root, "Web").text = web
    if dataissue["results"]["character_credits"]:
        characters = [character["name"]
                      for character in dataissue["results"]["character_credits"]]

        ET.SubElement(root, "Characters").text = ", ".join(characters)
    if dataissue["results"]["team_credits"]:
        teams = [team["name"] for team in dataissue["results"]["team_credits"]]

        ET.SubElement(root, "Teams").text = ", ".join(teams)
    tree = ET.ElementTree(root)
    from xml.dom import minidom
    xml = minidom.parseString(ET.tostring(root)).toprettyxml(indent="\t")
    ic(xml)
    filename = f'{loader.temporal}/ComicInfo.xml'
    tree.write(filename, encoding="utf-8", xml_declaration=True)


def generatexml(dic, issuenumber):  # sourcery skip: remove-redundant-if
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36"
    }
    url = f"https://comicvine.gamespot.com/api/volume/{dic['slug']}/?api_key=dcb22bb374f04e7217eaca81f2fcfffbe5062e42&format=json"
    responsevolume = requests.get(url, headers=headers)
    datavolume = responsevolume.json()
    for issue in datavolume["results"]["issues"]:
        if issue["issue_number"] == issuenumber:
            url = f"https://comicvine.gamespot.com/api/issue/4000-{issue['id']}/?api_key=dcb22bb374f04e7217eaca81f2fcfffbe5062e42&format=json"
            responseissue = requests.get(url, headers=headers)
            dataissue = responseissue.json()
            web = issue["site_detail_url"]
            break
    if dataissue:
        treeelement(datavolume, dataissue, web)


def loadxml():
    comicinfo = f"{loader.temporal}/ComicInfo.xml"
    with open(comicinfo, "r") as xml_obj:
        # coverting the xml data to Python dictionary
        my_dict = xmltodict.parse(xml_obj.read())
        # closing the file
    xml_obj.close()
    return my_dict


def generatecbz(my_dict, nombre):
    destino = f'/media/cristian/Datos/Comics/Reader/{my_dict["ComicInfo"]["Publisher"]}/{my_dict["ComicInfo"]["Series"]} ({my_dict["ComicInfo"]["Volume"]})'
    destino = destino.replace(":", "")
    destino = destino.replace("\\", " ")
    destino = destino.replace("?", "")
    ic(destino)
    if not os.path.exists(destino):
        os.makedirs(destino)
    if not os.path.exists(f"{destino}/poster.jpg") and my_dict["ComicInfo"]["Publisher"] in ["Marvel", "Delcourt", "DC Comics"]:
        getposter(my_dict, destino)
    archivos = glob.glob(f"{loader.temporal}/**/*.*", recursive=True)
    archivos.sort()
    cbz = f'{destino}/{my_dict["ComicInfo"]["Series"]} ({my_dict["ComicInfo"]["Volume"]}) Issue #{"{:0>4}".format(my_dict["ComicInfo"]["Number"])}.cbz'
    cbz = cbz.replace(":", "")
    cbz = cbz.replace("\\", " ")
    cbz = cbz.replace("?", "")
    zipobje = ZipFile(cbz, "w")
    for archivos2 in archivos:
        ruta, nombrearchivo = os.path.split(archivos2)
        zipobje.write(archivos2, basename(nombrearchivo))
    zipobje.close()
    loader.mensaj.append(f"{nombre}\n\n")
    sendmsgtelegram.sendmsg(
        loader.secrets["token"], loader.secrets["chatid"], loader.mensaj)
    sendmsgdiscord.sendmsg(
        loader.secrets["disdcordwebhook"], loader.mensaj)


def main():
    manually = [
        {
            "source": "/media/cristian/Datos/Comics/Tachiyomi/ReadComicOnline (EN)/Batman (2016)",
            "nombre": "Batman #125",
            "url": "https://getcomics.info/links.php/b4GtGnFTVS1fQiO8H3gLRvdZcrgLHchLZOy3ym0+HYyqwx8Qay99GAHHCQDNok6s1widLoHyHuBokxudlbSAlfeglxW1mG+yRqiuSHKgaKY=:U1/5vWzxKMvtM0IfhVZyHg==",
        }
    ]
    for comic in manually:
        r = requests.get(comic["url"], allow_redirects=True)
        if r.status_code == 200:
            open(
                f'{loader.tdescargas}/{comic["nombre"]}.cbr', 'wb').write(r.content)
            ic(f'Descargado: {comic["nombre"]}')
        if os.path.exists(f'{loader.tdescargas}/{comic["nombre"]}.cbr'):
            if os.path.exists(loader.temporal):
                try:
                    shutil.rmtree(loader.temporal)
                except Exception:
                    ic("Error while deleting directory")
            try:
                os.mkdir(loader.temporal)
            except OSError:
                ic(f"Creation of the directory {loader.temporal} failed")
            patoolib.extract_archive(
                f'{loader.tdescargas}/{comic["nombre"]}.cbr', outdir=loader.temporal)
            ic(f'Extraido: {comic["nombre"]}')
            issuenumber = comic["nombre"].split("#")[1]
            generatexml(loader.mangas[comic["source"]], issuenumber)
            my_dict = loadxml()
            if historial.historial(
            loader.history, "{:0>4}".format(issuenumber), loader.mangas[comic["source"]], loader.komgabooksid) == True:
                generatecbz(my_dict, comic["nombre"])
            loader.save()
            try:
                shutil.rmtree(loader.temporal)
            except Exception:
                ic("Error while deleting directory")
            try:
                os.remove(f'{loader.tdescargas}/{comic["nombre"]}.cbr')
            except Exception:
                ic("Error while deleting file")
        else:
            ic(f'No se encontro el comic: {comic["nombre"]}')
    scankomgalibrary.scankomgalibrary(loader.mensaj, loader.mensaj2,
                               loader.secrets["komgauser"], loader.secrets["komgapass"], loader.secrets)
