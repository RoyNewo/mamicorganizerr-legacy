import scrapy
from scrapy.crawler import CrawlerProcess
import cfscrape
import logging
from Test.ninemanga import filterchapter
from icecream import ic

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
            chapter_url = a.xpath(".//@href").extract_first()
            chapter_title = a.xpath(".//@title").extract_first()
            # ic(chapter_url, chapter_title)
            caplist.append([chapter_title, chapter_url])
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
            
            token, agent = cfscrape.get_tokens(url=str(chapter_url).replace(".html", "-10-1.html?waring=1"))
            self.token = token
            self.agent = agent
            print(self.agent)
            yield scrapy.Request(
                url=chapter_url,
                callback=self.parseimages,
                cookies=self.token,
                headers={"User-Agent": self.agent},
            )

    def parseimages(self, response):
        ic(response.xpath('//div[@class="changepage"]')[0].xpath('.//select/option/@value').getall())
        
        # dato = str(
        #     response.xpath(".//script")[0].xpath(".//@type").extract_first()
        # ).replace("-text/javascript", "")
        # print(dato)
        # scriptxpath = ".//script[@type='" + dato + "-application/javascript']"
        # # for script in response.xpath(".//script"):
        # #     print(script.xpath(".//@type").extract_first())
        # imagenes = (
        #     str(response.xpath(scriptxpath)[-1].xpath("string(.)").extract())
        #     .replace(" ", "")
        #     .split("\\r\\n")
        # )
        # print(imagenes)
        # print(response)


def main():
    proc = CrawlerProcess()
    proc.crawl(
        MangaChapterSpider,
        base_url="https://es.ninemanga.com/manga/Re%3AZero%20kara%20Hajimeru%20Isekai%20Seikatsu%20%28Novela%29.html?waring=1",
    )
    proc.start()
    print(caplist)
    manga = {
        "destino": "/home/data/Comics/Reader/Media Factory/Re Zero kara Hajimeru Isekai Seikatsu Novela (2012)",
        "name": "Re Zero kara Hajimeru Isekai Seikatsu (2014) Issue #",
        "funcion": "NineMangaEs (ES)",
        "provider": "NineMangaEs (ES)",
        "slug": "re-zero-kara-hajimeru-isekai-seikatsu",
        "Series": "Re Zero kara Hajimeru Isekai Seikatsu",
        "Volume": "2012",
        "Publisher": "Media Factory",
        "komga_serie_id": "02TA7PYNBB6WN"
    }
    for cap in caplist:

        ic(manga["name"] , filterchapter(cap[0], manga), cap[1])


if __name__ == "__main__":
    main()
