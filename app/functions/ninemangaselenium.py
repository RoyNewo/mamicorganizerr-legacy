# instalar firefox y geckodriver y selenium

# https://es.ninemanga.com/manga/Fire%20Punch.html?waring=1
# /html/body/div[2]/div/div[3]
# //*[@id="sub_vol_ul_0"]

# //*[@id="manga_pic_1"]

# //*[@id="page"]
# //*[@id="sub_vol_ul_100"]

# <ul class="sub_vol_ul" id="sub_vol_ul_0">
# //*[@id="manga_pic_6"], /html/body/center/table, /html/body/center /html/body/center/table/tbody/tr/td[2]/div

# <a class="chapter_list_a" href="https://es.ninemanga.com/chapter/Kumo%20Desu%20ga-%20Nani%20ka%3F/1096363.html" title="Kumo Desu ga Nani ka? 5" target="_blank">Kumo Desu ga Nani ka? 5</a>


from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from PIL import Image
import requests
import organizer as organizar
import os
import json
import shutil

mensaj = []
mensaj2 = []
mangadic = {
    "destino": "/home/data/Comics/Reader/Shueisha/Psyren (2007)/",
    "name": "Psyren (2007) Issue #",
    "funcion": "NineMangaEs (ES)",
    "provider": "NineMangaEs (ES)",
    "slug": "psyren",
    "Series": "Psyren",
    "Volume": "2007",
    "Publisher": "Shueisha",
    "ninemanga": "Psyren.html",
}
with open("/opt/tachiyomimangaexporter/history.json") as json_file3:
    history = json.load(json_file3)
infocaps = []
warning = "?waring=1"
base = "https://es.ninemanga.com"
mangabase = "/manga/"
chapterbase = "/chapter/"
mangatitle = mangadic["ninemanga"]
organizar.folderinit(mangadic)
tdescargas = "/home/data/Comics/Descargas/"
deletefolder = "Error while deleting directory"

options = Options()
options.headless = True
# options.add_argument("--no-sandbox")
# options.add_argument("--window-size=1920,1200")
# profile = webdriver.FirefoxProfile()
# profile.set_preference("network.http.pipelining", True)
# profile.set_preference("network.http.proxy.pipelining", True)
# profile.set_preference("network.http.pipelining.maxrequests", 8)
# profile.set_preference("content.notify.interval", 500000)
# profile.set_preference("content.notify.ontimer", True)
# profile.set_preference("content.switch.threshold", 250000)
# profile.set_preference(
#     "browser.cache.memory.capacity", 65536
# )  # Increase the cache capacity.
# profile.set_preference("browser.startup.homepage", "about:blank")
# profile.set_preference(
#     "reader.parse-on-load.enabled", False
# )  # Disable reader, we won't need that.
# profile.set_preference("browser.pocket.enabled", False)  # Duck pocket too!
# profile.set_preference("loop.enabled", False)
# profile.set_preference(
#     "browser.chrome.toolbar_style", 1
# )  # Text on Toolbar instead of icons
# profile.set_preference(
#     "browser.display.show_image_placeholders", False
# )  # Don't show thumbnails on not loaded images.
# profile.set_preference(
#     "browser.display.use_document_colors", False
# )  # Don't show document colors.
# profile.set_preference(
#     "browser.display.use_document_fonts", 0
# )  # Don't load document fonts.
# profile.set_preference("browser.display.use_system_colors", True)  # Use system colors.
# profile.set_preference("browser.formfill.enable", False)  # Autofill on forms disabled.
# profile.set_preference(
#     "browser.helperApps.deleteTempFileOnExit", True
# )  # Delete temprorary files.
# profile.set_preference("browser.shell.checkDefaultBrowser", False)
# profile.set_preference("browser.startup.homepage", "about:blank")
# profile.set_preference("browser.startup.page", 0)  # blank
# profile.set_preference(
#     "browser.tabs.forceHide", True
# )  # Disable tabs, We won't need that.
# profile.set_preference("browser.urlbar.autoFill", False)  # Disable autofill on URL bar.
# profile.set_preference(
#     "browser.urlbar.autocomplete.enabled", False
# )  # Disable autocomplete on URL bar.
# profile.set_preference(
#     "browser.urlbar.showPopup", False
# )  # Disable list of URLs when typing on URL bar.
# profile.set_preference("browser.urlbar.showSearch", False)  # Disable search bar.
# profile.set_preference("extensions.checkCompatibility", False)  # Addon update disabled
# profile.set_preference("extensions.checkUpdateSecurity", False)
# profile.set_preference("extensions.update.autoUpdateEnabled", False)
# profile.set_preference("extensions.update.enabled", False)
# profile.set_preference("general.startup.browser", False)
# profile.set_preference("plugin.default_plugin_disabled", False)
# profile.set_preference("permissions.default.image", 2)  # Image load disabled again


driver = webdriver.Firefox(options=options)
# Obtener todos los capitulos de un manga
driver.get(base + mangabase + mangatitle + warning)
# driver.get("https://es.ninemanga.com/manga/Fire%20Punch.html?waring=1")
# driver.get("https://es.ninemanga.com/manga/KOMI-SAN%20WA%20KOMYUSHOU%20DESU.html?waring=1")
manganame = str(
    driver.find_element_by_xpath("/html/body/div[2]/div/div[2]/ul/li[1]/span").text
).replace(" Manga", "")
if not os.path.exists(tdescargas + manganame):
    os.makedirs(tdescargas + manganame)
mangachapters = driver.find_element_by_xpath("/html/body/div[2]/div/div[3]")
listas = mangachapters.find_elements_by_class_name("sub_vol_ul")
for ele in listas:
    capitulo = ele.find_elements_by_class_name("chapter_list_a")
    for cap in capitulo:
        # print(
        #     cap.text, cap.get_attribute("href"), cap.find_element_by_xpath("./..").text
        # )
        # print(cap.get_attribute("href"))
        infocaps.append(
            {
                "url": cap.get_attribute("href"),
                "titulo": cap.text,
                "fecha": cap.find_element_by_xpath("./..").text,
            }
        )
# Obtener todas las paginas de un capitulo hay que tener en cuenta que no este vacio que a veces hay mangas que no tienen nada
for infocap in infocaps:
    if not os.path.exists(tdescargas + manganame + "/" + infocap["titulo"]):
        os.makedirs(tdescargas + manganame + "/" + infocap["titulo"])
    capurl = str(infocap["url"]).replace(".html", "-10-1.html" + warning)
    driver.get(capurl)
    # driver.get("https://es.ninemanga.com/chapter/Fire%20Punch/531897-1.html?waring=1")
    s = driver.find_element_by_xpath('//*[@id="page"]')
    op = [x for x in s.find_elements_by_tag_name("option")]
    contador = 0
    for numero, element in enumerate(op):
        pagina = base + element.get_attribute("value") + warning
        print(pagina)
        driver2 = webdriver.Firefox(options=options)
        driver2.get(pagina)

        # Obtener el enlace de una imagen y convertirla de webp a jpeg
        imagenes = driver2.find_elements_by_class_name("pic_box")
        listaimagenes = [
            div.find_element_by_tag_name("img").get_attribute("src") for div in imagenes
        ]
        # listaimagenes = imagenes.find_elements_by_tag_name("img")
        # listaurl = [imagen.get_attribute("src") for imagen in listaimagenes]
        driver2.quit()
        for count, imagen in enumerate(listaimagenes):
            print(imagen)
            im = Image.open(requests.get(imagen, stream=True).raw).convert("RGB")
            imageroute = (
                tdescargas
                + manganame
                + "/"
                + infocap["titulo"]
                + "/"
                + "{:0>2}".format(contador)
                + ".jpg"
            )
            im.save(imageroute, "jpeg")
            contador += 1
    organizar.organizer(
        [manganame, infocap["titulo"]],
        mangadic,
        tdescargas + manganame + "/" + infocap["titulo"] + "/",
        mensaj,
        mensaj2,
        history,
    )
try:
    shutil.rmtree(tdescargas + manganame)
except OSError:
    print(deletefolder)
driver.quit()
