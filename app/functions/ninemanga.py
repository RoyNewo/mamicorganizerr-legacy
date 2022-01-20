import scrapy
from scrapy.crawler import CrawlerProcess
import cfscrape
import logging
from manga_py.util import main as mangapimain
import argparse

logging.getLogger("scrapy").propagate = False  # Deshabilitamos los mensajes

caplist = []


class MangaChapterSpider(scrapy.Spider):

    name = "MangaChapterSpider"

    def start_requests(self):
        url = self.base_url  # url inicial (lista capitulos)
        # Bypass para cloudflare
        token, agent = cfscrape.get_tokens(url=url)
        self.token = token
        self.agent = "Mozilla/5.0 (Windows NT 10.0; WOW64) Gecko/20100101 Firefox/75"
        self.max = 2
        self.pages = 0
        yield scrapy.Request(
            url=url,
            callback=self.parsechapters,
            cookies=token,
            headers={"User-Agent": agent},
        )

    def parsechapters(self, response):
        for a in response.xpath('.//a[@class="chapter_list_a"]'):
            # chapter_url = a.xpath(".//@href").extract_first()
            chapter_title = a.xpath(".//@title").extract_first()
            # print(chapter_url, chapter_title)
            caplist.append(chapter_title)
        # print(a)
        # print(
        #     response.xpath('.//a[@class="chapter_list_a"]')[0]
        #     .xpath(".//@href")
        #     .extract_first()
        # )
        # chapterurl = (
        #     response.xpath('.//a[@class="chapter_list_a"]')[0]
        #     .xpath(".//@href")
        #     .extract_first()
        # )
        # chapterurl = "https://es.ninemanga.com/chapter/KOMI-SAN%20WA%20KOMYUSHOU%20DESU/1163928-10-1.html?waring=1"
        # token, agent = cfscrape.get_tokens(url=chapterurl)
        # self.token = token
        # self.agent = agent
        # print(self.agent)
        # yield scrapy.Request(
        #     url=chapterurl,
        #     callback=self.parseimages,
        #     cookies=self.token,
        #     headers={"User-Agent": self.agent},
        # )

    # def parseimages(self, response):
    #     dato = str(
    #         response.xpath(".//script")[0].xpath(".//@type").extract_first()
    #     ).replace("-text/javascript", "")
    #     print(dato)
    #     scriptxpath = ".//script[@type='" + dato + "-application/javascript']"
    #     # for script in response.xpath(".//script"):
    #     #     print(script.xpath(".//@type").extract_first())
    #     imagenes = (
    #         str(response.xpath(scriptxpath)[-1].xpath("string(.)").extract())
    #         .replace(" ", "")
    #         .split("\\r\\n")
    #     )
    #     print(imagenes)
    # print(response)


def main():
    proc = CrawlerProcess()
    proc.crawl(
        MangaChapterSpider,
        base_url="https://es.ninemanga.com/manga/Fire%20Punch.html?waring=1",
    )
    proc.start()
    print(caplist)
    argparse.Namespace(URL="https://es.ninemanga.com/manga/Fire%20Punch.html")
    mangapimain()


if __name__ == "__main__":
    main()
