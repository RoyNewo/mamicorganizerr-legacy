import requests
import cfscrape
from bs4 import BeautifulSoup
from icecream import ic
from Test.ninemanga import filterchapter
from PIL import Image
import os

def main():
    base_url = "https://es.ninemanga.com"

    manga_url="https://es.ninemanga.com/manga/Re%3AZero%20kara%20Hajimeru%20Isekai%20Seikatsu%20%28Novela%29.html?waring=1"
    path = "/media/cristian/Datos/Comics/Tachiyomi/NineMangaEs (ES)/Re_Zero kara Hajimeru Isekai Seikatsu (Novela)/"
    manga = {
            "destino": "/media/cristian/Datos/Comics/Reader/Media Factory/Re Zero kara Hajimeru Isekai Seikatsu Novela (2012)",
            "name": "Re Zero kara Hajimeru Isekai Seikatsu (2014) Issue #",
            "funcion": "NineMangaEs (ES)",
            "provider": "NineMangaEs (ES)",
            "slug": "re-zero-kara-hajimeru-isekai-seikatsu",
            "Series": "Re Zero kara Hajimeru Isekai Seikatsu",
            "Volume": "2012",
            "Publisher": "Media Factory",
            "komga_serie_id": "02TA7PYNBB6WN"
        }
    headers = {
        'User-Agent': "Mozilla/5.0 (Windows NT 10.0; WOW64) Gecko/20100101 Firefox/75"
    }
    scraper = cfscrape.create_scraper()
    response = scraper.get(manga_url, headers=headers)
    soup = BeautifulSoup(response.text, 'lxml')
    enlaces = soup.find_all('a', class_="chapter_list_a")
    # for enlace in enlaces:
    #     ic(enlace.attrs)
    #     ic(manga["name"] , filterchapter(enlace.attrs['title'], manga), enlace.attrs['href'])
    chaptername = str(filterchapter(enlaces[0].attrs['title'], manga)) + '/'
    dfolder = f'{path}/{chaptername}'
    if not os.path.exists(dfolder):
        os.makedirs(dfolder)

    chapter = scraper.get(str(enlaces[0].attrs['href'].replace(".html", "-10-1.html?waring=1")), headers=headers)
    chaptersoup = BeautifulSoup(chapter.text, 'lxml')
    # ic(chaptersoup)
    chapterpagesdiv = chaptersoup.find('div', class_="changepage")
    contador = 0
    for option in chapterpagesdiv.find_all("option"):
        ic(option['value'])
        chapterimagesurl = base_url + option['value'] + "?waring=1"
        # chapterimages = scraper.get(chapterimagesurl, headers=headers)
        chapterimagessoup = BeautifulSoup(scraper.get(chapterimagesurl, headers=headers).text, 'lxml')
        for img in chapterimagessoup.find_all('img', class_='manga_pic'):
            ic(img.attrs)
            im = Image.open(requests.get(img.attrs["src"], stream=True).raw).convert("RGB")
            imagenumber = int(img.attrs["i"]) + contador
            imageroute = (path + chaptername + "{:0>2}".format(str(imagenumber))
                    + ".jpg" )
            im.save(imageroute, "jpeg")
        contador += 10
