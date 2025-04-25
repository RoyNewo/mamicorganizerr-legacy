import time
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from PIL import Image
import requests
from bs4 import BeautifulSoup
from icecream import ic
from Test.ninemanga import filterchapter
from functions import organizer
import os
import json
import shutil
import cloudscraper
import sys
import traceback

driver = ''

def my_exception_hook(type, value, tb):    
    traceback_details = "\n".join(traceback.extract_tb(tb).format())
    error_msg = (
        "Mangaexporter: An exception has been raised outside of a try/except!!!\n"
        f"Type: {type}\n"
        f"Value: {value}\n"
        f"Traceback: {traceback_details}"
    )
    ic(error_msg)
    driver.quit()

    

def main():
    sys.excepthook = my_exception_hook
    global driver
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
    options = Options()
    options.headless = True
    driver = webdriver.Firefox(options=options)
    
    driver.get(manga_url)
    html = driver.page_source
    soup = BeautifulSoup(html, 'lxml')
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
        titulo= children[0].find('h4', class_="mt-2 text-truncate").attrs['title']
        href = children[1].find('a', class_="btn btn-default btn-sm").attrs['href']
        ic(titulo, href)
        capitulos.append([titulo,href])
        del children[:2]
    chaptername = f'{str(filterchapter(capitulos[0][0], manga))}/'
    dfolder = f'{path}/{chaptername}'
    if not os.path.exists(dfolder):
        os.makedirs(dfolder)
    selector = f"a[href='{capitulos[0][1]}']"
    time.sleep(5)
    driver.find_element_by_css_selector(selector).click()
    time.sleep(5)
    with open("response.html", "w") as f:
        f.write(driver.page_source)
    currenturl = driver.current_url
    currenturl = currenturl.replace('paginated/1', 'cascade')
    selector = f"a[href='{currenturl}']"
    driver.find_element_by_css_selector(selector).click()
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    html = driver.page_source
    with open("response2.html", "w") as f:
        f.write(driver.page_source)
    ic(BeautifulSoup(html, 'lxml'))
    driver.quit()