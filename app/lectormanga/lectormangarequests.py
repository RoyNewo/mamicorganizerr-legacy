import requests
from requests_toolbelt import user_agent
import cloudscraper
from bs4 import BeautifulSoup
from icecream import ic
from Test.ninemanga import filterchapter
from PIL import Image
import os


def main():
    base_url = "https://lectormanga.com"

    manga_url = "https://lectormanga.com/library/manga/9237/kono-subarashii-sekai-ni-shukufuku-wo"
    path = "/home/data/Comics/Buffer/Dragon Age/Kono Subarashii Sekai Ni Shukufuku Wo (2014)"
    manga = {
        "destino": "/home/data/Comics/Reader/Dragon Age/Kono Subarashii Sekai Ni Shukufuku Wo (2014)",
        "name": "Kono Subarashii Sekai Ni Shukufuku Wo (2014) Issue #",
        "funcion": "LectorManga (ES)",
        "provider": "LectorManga (ES)",
        "slug": "kono-subarashii-sekai-ni-shukufuku-wo",
        "Series": "Kono Subarashii Sekai Ni Shukufuku Wo",
        "Volume": "2014",
        "Publisher": "Dragon Age",
        "komga_serie_id": "07AFWR8MGY8FR",
        "web_url": "https://lectormanga.com",
        "manga_url": "/library/manga/9237/kono-subarashii-sekai-ni-shukufuku-wo"
    }
    headers = {
        'User-Agent': "Mozilla/5.0 (Windows NT 10.0; WOW64) Gecko/20100101 Firefox/75"
    }
    scraper = cloudscraper.create_scraper(
        interpreter='nodejs',
        captcha={
            'provider': 'deathbycaptcha',
            'username': 'roynewo',
            'password': 'Stormaggedon13101992-',
        }
    )
    response = scraper.get(manga_url, headers=headers)
    soup = BeautifulSoup(response.text, 'lxml')
    ic(soup)
    chapters = soup.find('div', id="chapters")
    children = chapters.findChildren(recursive=False)
    ic(len(children))
    childrenocultos = children[-2].findChildren(recursive=False)
    ic(len(childrenocultos))
    del children[-2:]
    for child in childrenocultos:
        children.append(child)
    ic(len(children), children)
    capitulos = []
    while len(children) > 0:
        titulo = children[0].find(
            'h4', class_="mt-2 text-truncate").attrs['title']
        href = children[1].find(
            'a', class_="btn btn-default btn-sm").attrs['href']
        ic(titulo, href)
        capitulos.append([titulo, href])
        del children[:2]
    chaptername = f'{str(filterchapter(capitulos[0][0], manga))}/'
    dfolder = f'{path}/{chaptername}'
    if not os.path.exists(dfolder):
        os.makedirs(dfolder)
    chapter = scraper.get(
        capitulos[0][1], headers=headers, allow_redirects=False)
    ic(chapter.headers['Location'])
    # chaptersoup = BeautifulSoup(chapter.text, 'lxml')
    # ic(chaptersoup)
