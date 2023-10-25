import scrapy
from scrapy.crawler import CrawlerProcess
import json
import os
import functions.organizer as organizar
import requests
from icecream import ic

pendientes = []


class explosmspider(scrapy.Spider):
    name = "explosm"

    start_urls = ["https://explosm.net/comics/latest"]

    def __init__(self, ultimo=None):
        self.ultimo = ultimo

    def parse(self, response):
        global pendientes
        url = '//div[@class="MainComic__ComicImage-sc-ndbx87-2 lmqaxm"]/span/img/@src'
        nombre = response.xpath(
            '//div[@class="Author__Right-sc-1w0z97f-2 HhxjY"]/p[1]/text()'
        ).get()
        yield {"nombre": nombre, "url": response.xpath(url).get()}
        next_page = response.xpath(
            '//div[@class="ComicSelector__Container-sc-tx5aab-0 eudaLQ"]/a[1]/@href'
        ).get()
        if nombre != self.ultimo:
            pendientes.append([nombre, response.xpath(url).get()])
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse)


class explosmspidernuevo(scrapy.Spider):
    name = "explosm"

    start_urls = ["https://explosm.net/comics/latest"]

    def __init__(self, ultimo=None):
        self.ultimo = ultimo

    def parse(self, response):
        global pendientes
        url = '//div[@class="MainComic__ComicImage-sc-ndbx87-2 lmqaxm"]/span/img/@src'
        nombre = response.xpath(
            '//div[@class="Author__Right-sc-1w0z97f-2 HhxjY"]/p[1]/text()'
        ).get()
        yield {"nombre": nombre, "url": response.xpath(url).get()}
        next_page = response.xpath(
            '//div[@class="ComicSelector__Container-sc-tx5aab-0 eudaLQ"]/a[1]/@href'
        ).get()
        if nombre[:4] == self.ultimo:
            pendientes.append([nombre, response.xpath(url).get()])
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse)


def cyanide(manga):
    rutahistorial = "/opt/tachiyomimangaexporter/history.json"
    with open(rutahistorial) as json_file:
        history = json.load(json_file)
    with open("/opt/tachiyomimangaexporter/mangas.json") as json_file2:
        mangas = json.load(json_file2)
    with open("/opt/tachiyomimangaexporter/secrets.json") as json_file3:
        secrets = json.load(json_file3)

    nombre = mangas[manga]["Series"]
    volumen = mangas[manga]["Volume"]
    process = CrawlerProcess()
    if nombre in history:
        ultimo = str(list(history[nombre])[-1])
        process.crawl(explosmspider, ultimo=ultimo)
    else:
        history[nombre] = {}
        if not os.path.exists(mangas[manga]["destino"]):
            os.makedirs(mangas[manga]["destino"])
        process.crawl(explosmspidernuevo, ultimo=volumen)
    process.start()
    ic(pendientes)
    if pendientes:
        mensaj = []
        mensaj2 = []
        deletefolder = "Error while deleting directory"
        tdescargas = "/media/cristian/Datos/Comics/Descargas"
        for capitulo in reversed(pendientes):
            ic(capitulo)
            if capitulo[0][:4] == volumen:
                archivo = capitulo[1].split("/")[-1]
                os.makedirs(f"{tdescargas}/{capitulo[0]}")
                path = f"{tdescargas}/{capitulo[0]}/{archivo}"
                resp = requests.get(capitulo[1])
                data = bytearray(resp.content)
                with open(path, "wb") as fin:
                    # writing decryption data in image
                    fin.write(data)
                cbz = (
                    mangas[manga]["destino"]
                    + "/"
                    + mangas[manga]["name"]
                    + capitulo[0]
                    + ".cbz"
                )
                organizar.newinhistory(mangas[manga], f"{tdescargas}/{capitulo[0]}", capitulo[0], deletefolder, cbz, False, mensaj2, mensaj, secrets)

                history[nombre][capitulo[0]] = mangas[manga]["funcion"]
                with open(rutahistorial, "w") as outfile:
                    json.dump(history, outfile)
                mensaj = []
                mensaj2 = []
        organizar.scankomgalibrary(
            mensaj, mensaj2, secrets["komgauser"], secrets["komgapass"], secrets
        )
        # organizar.send(mensaj, mensaj2)
