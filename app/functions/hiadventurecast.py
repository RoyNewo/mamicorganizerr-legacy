import scrapy
from scrapy.crawler import CrawlerProcess
from datetime import datetime
from icecream import ic
import requests
from scrapy.http import request
import json
import os
import organizer as organizar

pendientes = []


def convert_date(text):
    date = datetime.strptime(text[:10], "%Y-%m-%d")
    return str(date.strftime("%Y.%m.%d"))

def same_day_chapters(nombre, history):
    i = 2
    nuevonombre = nombre + '-' + str(i)
    while nuevonombre in history:
        i += 1
        nuevonombre = nombre + '-' + str(i)
    return nuevonombre


class hiadventurecast(scrapy.Spider):
    name = "hiadventurecast"

    start_urls = ["https://hiadventurecast.com/category/webcomics/"]

    def __init__(self, ultimo=None):
        self.ultimo = ultimo

    def parse(self, response):
        global pendientes
        if self.ultimo is None:
            for i in range(
                len(response.xpath('//*[@id="block-wrap-41210"]/div/div/div/article'))
            ):
                prefijo = (
                    '//*[@id="block-wrap-41210"]/div/div/div/article['
                    + str(i + 1)
                    + "]/div/div[2]/"
                )
                fecha = prefijo + "div[2]/span[4]/time/@datetime"
                url = prefijo + "div[1]/h3/a/@href"
                nomcap = convert_date(response.xpath(fecha).get())
                request_obeject = requests.get(response.xpath(url).get())
                response_object = scrapy.Selector(request_obeject)
                image = (
                    response_object.xpath('//div[@class="elementor-widget-container"]')
                    .css("img")
                    .xpath("@data-lazy-srcset")
                    .getall()
                )
                imagenes = [img.split(",")[0].split(" ")[0] for img in image]
                pendientes.append([nomcap, imagenes])
        else:
            for i in range(
                len(response.xpath('//*[@id="block-wrap-41210"]/div/div/div/article'))
            ):
                prefijo = (
                    '//*[@id="block-wrap-41210"]/div/div/div/article['
                    + str(i + 1)
                    + "]/div/div[2]/"
                )
                fecha = prefijo + "div[2]/span[4]/time/@datetime"
                url = prefijo + "div[1]/h3/a/@href"
                nomcap = convert_date(response.xpath(fecha).get())
                if nomcap == self.ultimo:
                    break
                request_obeject = requests.get(response.xpath(url).get())
                response_object = scrapy.Selector(request_obeject)
                image = (
                    response_object.xpath('//div[@class="elementor-widget-container"]')
                    .css("img")
                    .xpath("@data-lazy-srcset")
                    .getall()
                )
                imagenes = [img.split(",")[0].split(" ")[0] for img in image]
                pendientes.append([nomcap, imagenes])


def hac():
    rutahistorial = "/opt/tachiyomimangaexporter/history.json"
    with open(rutahistorial) as json_file:
        history = json.load(json_file)
    with open("/opt/tachiyomimangaexporter/secrets.json") as json_file3:
        secrets = json.load(json_file3)

    manga = {
        "destino": "/media/cristian/Datos/Comics/Reader/HiAdventureCast",
        "name": "HiAdventureCast Issue #",        
        "funcion": "HiAdventureCast",
        "slug": "undefined",
        "Series": "HiAdventureCast",
        "Volume": "2019",
        "Publisher": "HiAdventureCast",
    }


    process = CrawlerProcess()
    if manga["Series"] in history:
        ultimo = str(list(history[manga["Series"]])[-1])
        process.crawl(hiadventurecast, ultimo=ultimo)
    else:
        history[manga["Series"]] = {}
        if not os.path.exists(manga["destino"]):
            os.makedirs(manga["destino"])
        process.crawl(hiadventurecast)
    process.start()
    ic(pendientes)
    if pendientes:
        mensaj = []
        mensaj2 = []
        deletefolder = "Error while deleting directory"
        tdescargas = "/media/cristian/Datos/Comics/Descargas"
        for capitulo in reversed(pendientes):
            if capitulo[0] in history[manga["Series"]]:
                capitulo[0] = same_day_chapters(capitulo[0], history[manga["Series"]])

            os.makedirs(tdescargas + "/" + capitulo[0])
            if capitulo[1]:
                for i, cap in enumerate(range(len(capitulo[1])), start=1):    
                    archivo = capitulo[1][cap].split("/")[-1].split(".")[-1]
                    num = "{:0>4}".format(i)
                    path = tdescargas + "/" + capitulo[0] + "/" + num + "." + archivo
                    resp = requests.get(capitulo[1][cap])
                    data = bytearray(resp.content)
                    with open(path, "wb") as fin:
                        # writing decryption data in image
                        fin.write(data)
                cbz = (
                    manga["destino"]
                    + "/"
                    + manga["name"]
                    + capitulo[0]
                    + ".cbz"
                )
                organizar.newinhistory(
                    manga,
                    tdescargas + "/" + capitulo[0],
                    capitulo[0],
                    deletefolder,
                    cbz,
                    False,
                    mensaj2,
                    mensaj,
                )                
                history[manga["Series"]][capitulo[0]] = manga["funcion"]
                with open(rutahistorial, "w") as outfile:
                    json.dump(history, outfile)
                mensaj = []
                mensaj2 = []
    organizar.scankomgalibrary(
        mensaj, mensaj2, secrets["komgauser"], secrets["komgapass"], secrets
    )
    # organizar.send(mensaj, mensaj2)



if __name__ == "__main__":
    hac()
