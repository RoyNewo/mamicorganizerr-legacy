import json
import os
import logging
from sys import stdout

logger = logging.getLogger(__name__)
fmt = "%(filename)-20s:%(lineno)-4d %(asctime)s %(message)s"
logging.basicConfig(
    level=logging.INFO, format=fmt, handlers=[logging.StreamHandler(stdout)]
)


def main():
    excludes = [
        "/media/cristian/Datos/Comics/Tachiyomi/automatic",
        "/media/cristian/Datos/Comics/Tachiyomi/Manually",
        "/media/cristian/Datos/Comics/Tachiyomi/Updates",
        "/media/cristian/Datos/Comics/Tachiyomi/backup",
    ]

    with open("/opt/tachiyomimangaexporter/mangas.json") as json_file:
        mangas = json.load(json_file)

    path = "/media/cristian/Datos/Comics/Tachiyomi"
    dirs = os.listdir(path)
    dirs.sort()
    for file1 in dirs:
        path2 = f"{path}/{file1}"
        if path2 not in excludes and os.path.isdir(path2):
            files = os.listdir(path2)
            for file2 in files:
                path3 = f"{path2}/{file2}"
                if path3 not in excludes and os.path.isdir(path3):
                    # logger.info(path3)
                    if path3 not in mangas:
                        logger.info(f"{path3} not in mangas")
                        mangas[path3] = {
                            "destino": "",
                            "name": "",
                            "funcion": "",
                            "provider": "",
                            "slug": "undefined",
                            "Series": "",
                            "Volume": "",
                            "Publisher": "",
                            "mangaid": "",
                            "portrait": "",
                            "komga_serie_id": ""}

    with open('/opt/tachiyomimangaexporter/mangas.json', "w") as mangas_file:
        json.dump(mangas, mangas_file, ensure_ascii=False)


if __name__ == "__main__":
    main()
