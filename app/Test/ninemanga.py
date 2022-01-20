from icecream import ic
import os
import json
from pathlib import Path
import requests
# import functions.organizer as organizar
import re
import sqlite3
from sqlite3 import Error



# SELECT * FROM mangas WHERE (source = 4097111295486074350 or source = 120391793502126753) and initialized = 1;
# https://en.ninemanga.com/manga/Ascendance+of+a+Bookworm+%7EI%27ll+Do+Anything+to+Become+a+Librarian%7E+Part+2+%E3%80%8CI%27ll+Become+a+Shrine+Maiden+for+Books%21%E3%80%8D.html
def filterchapter(webtitle, dic):
    tags = [
        "ep",
        "ch",
        "chapter",
        "chapterr",
        "chap",
        "episodio",
        "capitulo",
        "num",
        "issue",
        "generations",
    ]

    numero = ""
    cadena = (
        webtitle.lower()
        .replace("ch.", "ch ")
        .replace(":", " ")
        .replace(u"núm.", "num ")
        .replace(u"ó", "o")
        .replace(u"á", "a")
        .replace(u"́é", "e")
        .replace(u"í", "i")
        .replace(u"ú", "u")
        .replace(u"ñ", "n")
        .replace(u"é", "e")
        .replace(u"“", "")
        .replace(u"”", "")
        .replace(u"«", "")
        .replace(u"»", "")
        .replace(u"ô", "o")
        .replace(u"â", "a")
        .replace(".hu", "")
        .replace(".lr", "")
        .replace("shueisha_", "")
        .replace("mangakakalot.com_", "")
        .replace("readmanganato.com_", "")
        .replace("_tmp", "tmp")
        .replace("_", " ")
        .replace("cap&iacute;tulo", "capitulo")
    )
    ic(webtitle)
    ic(cadena)
    # Vamos a comprobar primero si aparece las palabras clave donde el capitulo esta detras
    # Un bucle con enmuerate para tener indice y el valor de la lista
    # La lista es el string separado por espacios por lo que cada indice es una palabra
    for indx , palabra in enumerate(cadena.split()):
        if palabra in tags:
            numero = cadena.split()[indx + 1]
    if not numero:
        sintitulo = webtitle.lower().replace(dic.lower(), "")
        ic(dic.lower())
        ic(sintitulo)
        ic(sintitulo.split()[0])
        if (
            sintitulo.split()[0].isnumeric()
            or not sintitulo.split()[0].isnumeric()
            and "." in sintitulo.split()[0]
        ):
            numero = sintitulo.split()[0]
        else:
            numero = webtitle

    return numero

def create_connection(db_file):
    """create a database connection to the SQLite database
        specified by the db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Error as e:
        print(e)

    return conn

def select_all_tasks(conn):
    """
    Query all rows in the tasks table
    :param conn: the Connection object
    :return:
    """
    cur = conn.cursor()
    cur.execute("SELECT source, url, title FROM mangas WHERE (source = 4097111295486074350 or source = 120391793502126753) and initialized = 1")

    return cur.fetchall()

    



def ninemanga():
    log = {}
    conn = create_connection("/media/cristian/Datos/Comics/Buffer/manga-py/tachiyomi.db")
    with conn:
        print("2. Query all tasks")
        lista = select_all_tasks(conn)
    
    for iterable in lista:
        if iterable[0] == 4097111295486074350:
            url = 'https://es.ninemanga.com'        
        else:
            url = 'https://en.ninemanga.com'

        fullurl = url + iterable[1]

        if len(iterable[1].split('?')) == 1:
            fullurl = fullurl + '?waring=1'
        
        log[iterable[2]] = {}
        infofile = Path("/media/cristian/Datos/Comics/Buffer/manga-py/info.json")
        init = (
            'manga-py -f -u "Mozilla/5.0 (Windows NT 10.0; WOW64) Gecko/20100101 Firefox/75" --skip-incomplete-chapters --print-json --simulate ' + fullurl + ' > '
            + str(infofile)
        )
        os.system(init)
        if infofile.is_file():
            with open(infofile) as info_file:
                info = json.load(info_file)

            hearders = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) Gecko/20100101 Firefox/75",
                "Accept-Language": "es-ES,es;q=0.9,en;q=0.8,gl;q=0.7",
            }
            # manga = {
            #     "destino": "/media/cristian/Datos/Comics/Reader/Kodansha/Mokushiroku no Yonkishi (2021)/",
            #     "name": "Mokushiroku no Yonkishi (2021) Issue #",
            #     "funcion": "NineMangaEs (ES)",
            #     "provider": "NineMangaEs (ES)",
            #     "slug": "mokushiroku-no-yonkishi",
            #     "Series": "Mokushiroku no Yonkishi",
            #     "Volume": "2021",
            #     "Publisher": "Kodansha",
            # }
            for volume in info["volumes"]:
                n = requests.get(volume["url"], headers=hearders)
                al = n.text
                head = str(al[al.find("<TITLE>") + 7 : al.find("</TITLE>")])
                # ic(filterchapter(al[al.find("<TITLE>") + 7 : al.find("</TITLE>")], iterable[2]))
                log[iterable[2]][head] = filterchapter(head, iterable[2])
                ic(iterable[2], head, log[iterable[2]][head])
        with open("ninemanga.log", "w", encoding='utf8') as outfile:
            json.dump(log, outfile, ensure_ascii=False)


if __name__ == "__main__":
    ninemanga()