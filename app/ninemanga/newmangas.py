from logging import warning
import ninemanga.loader
import requests
from functions import sendmsgdiscord, sendmsgtelegram, filterchapters
from bs4 import BeautifulSoup
import cfscrape
import json
from icecream import ic

def main():
    log = {}
    scraper = cfscrape.create_scraper()
    ninemangalist = [key for key in ninemanga.loader.mangas if ninemanga.loader.mangas[key]['provider'] in ['NineMangaEs (ES)', 'NineMangaEn (EN)']]
    for manga in ninemangalist:
        ic(manga)
        if str(ninemanga.loader.mangas[manga]["manga_url"]).split('?')[-1] != ninemanga.loader.waring:
            waring = ninemanga.loader.mangas[manga]["manga_url"] + ninemanga.loader.waring
        else:
            waring = ninemanga.loader.mangas[manga]["manga_url"]
        manga_url = ninemanga.loader.mangas[manga]["web_url"] + waring
        chapterlistsoup = BeautifulSoup(scraper.get(manga_url, headers=ninemanga.loader.headers).text, 'lxml')
        #  compararlo con history para ver que falta para descargarlo, diferenciar cuando es texto y numero de filterchapters, metodo que envie una notificacion cuando un capitulo no cuadre, para luego corregirlo
        chapterlistenlaces = chapterlistsoup.find_all('a', class_="chapter_list_a")
        chapternumbers = []
        for enlace in chapterlistenlaces:
            # chapternumber = str(filterchapters.filterchapter(enlace.attrs['title'], manga)) + '/'
            chapternumbers.append(str(filterchapters.filterchapter(enlace.attrs['title'], ninemanga.loader.mangas[manga])))
        log[manga]=chapternumbers
    with open("ninenewmangas.log", "w", encoding='utf8') as outfile:
        json.dump(log, outfile, ensure_ascii=False)
    


