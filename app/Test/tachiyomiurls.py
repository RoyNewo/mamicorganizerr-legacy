from icecream import ic
import sqlite3
from sqlite3 import Error
import json


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
    cur.execute(
        "SELECT source, url, title FROM mangas WHERE  favorite = 1 and initialized = 1")

    return cur.fetchall()


def main():
    providers = {
        4097111295486074350: {"web_url": "https://es.ninemanga.com",
                              "provider": "NineMangaEs (ES)"
                              },
        120391793502126753: {"web_url": "https://en.ninemanga.com",
                             "provider": "NineMangaEn (EN)"
                             },
        2528986671771677900: {"web_url": "https://mangakakalot.com",
                              "provider": "NineMangaEn (EN)"
                              },
        8061953015808280611: {"web_url": "https://readcomiconline.li",
                              "provider": "ReadComicOnline (EN)"
                              },
        2522335540328470744: {"web_url": "https://www.webtoons.com",
                              "provider": "NineMangaEn (EN)"
                              },
        7925520943983324764: {"web_url": "https://lectormanga.com",
                              "provider": "LectorManga (ES)"
                              },
        4146344224513899730: {"web_url": "https://lectormanga.com",
                              "provider": "TuMangaOnline (ES)"
                              },
        2499283573021220255: {"web_url": "https://mangadex.org",
                              "provider": "MangaDex (ES-419)"
                              },
        4938773340256184018: {"web_url": "https://mangadex.org",
                              "provider": "MangaDex (ES-419)"
                              }
    }
    fallos = {}
    conn = create_connection(
        "/media/cristian/Datos/Comics/Buffer/databases/tachiyomi.db")
    with conn:
        print("2. Query all tasks")
        lista = select_all_tasks(conn)
    with open("/opt/tachiyomimangaexporter/mangas.json") as json_file:
        mangas = json.load(json_file)
    for iterable in lista:
        ic(iterable)
        booleana = False
        for key in mangas:
            if mangas[key]["Series"] in iterable[2] and providers[iterable[0]]['provider'] == mangas[key]["provider"]:
                ic(key)
                mangas[key]["web_url"] = providers[iterable[0]]["web_url"]
                mangas[key]["manga_url"] = iterable[1]
                booleana = True
                ic(mangas[key])
        if not booleana:
            fallos[iterable[1]] = {"manga": iterable[2],
                                   "provider": providers[iterable[0]]['provider']}
    ic(fallos)
    with open("tachiyomifallo.log", "w", encoding='utf8') as outfile:
        json.dump(fallos, outfile, ensure_ascii=False)
    with open("/opt/tachiyomimangaexporter/mangas.json", "w") as outfile:
        json.dump(mangas, outfile)


if __name__ == "__main__":
    main()
