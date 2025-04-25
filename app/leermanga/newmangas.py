import leermanga.loader
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


def main():
    global manga_url
    
    lista = [[leermanga.loader.mangas[manga]['Series'], manga] for manga in leermanga.loader.mangas]
    newmangas = {key[1]: leermanga.loader.mangas[key[1]] for key in sorted(lista, key=lambda x: x[0])}
    ninemangalist = [key for key in newmangas if newmangas[key]
                     ['provider'] in ['NineMangaEs (ES)', 'NineMangaEn (EN)']]
    for manga in ninemangalist:
        
        waring = leermanga.loader.mangas[manga]["manga_url"] + leermanga.loader.waring if str(
            leermanga.loader.mangas[manga]["manga_url"]).split('?')[-1] != leermanga.loader.waring else leermanga.loader.mangas[manga]["manga_url"]

        manga_url = leermanga.loader.mangas[manga]["web_url"] + waring
        ic(f'Revisando manga {leermanga.loader.mangas[manga]["Series"]} - {leermanga.loader.mangas[manga]["provider"]} - {manga_url}')
        # ic(urlmanga.text)
        # with open(f'/home/cristian/Github/mamicorganizerr-legacy/app/ninemanga/response/{leermanga.loader.mangas[manga]["Series"]}.json', 'w', encoding='utf-8') as f:
        #     json.dump(json_data, f, indent=4, ensure_ascii=False)
        # thejson = flaresolverr(manga_url)
        # ic(thejson['response'])

        capitulos = flaresolverr(manga_url)
        while 'solution' not in capitulos:
            capitulos = flaresolverr(manga_url)
        chapterlistsoup = BeautifulSoup(capitulos["solution"]['response'], 'lxml')
        chapterlistenlaces = chapterlistsoup.find_all(
            'a', class_="chapter_list_a")
        for enlace in chapterlistenlaces:
            checkchapter(enlace, manga)            
            ic(enlace, manga)
        
    organizer.scankomgalibrary(
        leermanga.loader.mensaj, leermanga.loader.mensaj2, leermanga.loader.secrets["komgauser"], leermanga.loader.secrets["komgapass"], leermanga.loader.secrets
    )
    # organizer.send(leermanga.loader.mensaj, leermanga.loader.mensaj2)