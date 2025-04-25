import leermanga.loader
import requests
from functions import sendmsg, filterchapters, historial, organizer
from bs4 import BeautifulSoup
import cfscrape
# import cfscrape
import json
from icecream import ic
import os
from PIL import Image
import re
manga_url = 'https://www.leer-manga.com/manga/blue-lock'
domain = 'https://www.leer-manga.com'

global scraper
scraper = cfscrape.create_scraper()

def getchapterpages(enlace, chapter):
    pass

def main():
    chapterlistsoup = BeautifulSoup(scraper.get(
            manga_url, headers=leermanga.loader.headers).text, 'lxml')
    chapterlistenlaces = chapterlistsoup.find_all(href=re.compile('scan'), class_="")
    # ic(chapterlistenlaces.get('href'))
    ic(chapterlistenlaces[0].get('href'))
    ic(chapterlistenlaces[0].find('h5').find(text=True, recursive=False))
    