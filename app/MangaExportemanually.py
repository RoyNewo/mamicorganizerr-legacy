import json
import requests
from requests.auth import HTTPBasicAuth
import os
import shutil
from functions.organizer import send, organizer, posterc, posterm


def main():

    manually = "/opt/tachiyomimangaexporter/manually.json"
    if os.path.exists(manually):

        with open(manually) as json_file4:
            mangas = json.load(json_file4)
        mensaj = []
        mensaj2 = []
        with open("/opt/tachiyomimangaexporter/secrets.json") as json_file2:
            secrets = json.load(json_file2)
        with open("/opt/tachiyomimangaexporter/history.json") as json_file3:
            history = json.load(json_file3)
        # manga = {
        #     "origen": "/media/cristian/Datos/Comics/Tachiyomi/Manually/Hollow Knight",
        #     "destino": "/media/cristian/Datos/Comics/Reader/Team Cherry/Hollow Knight Chapter One Quirrel (2017)",
        #     "name": "Hollow Knight Chapter One Quirrel (2017) Issue #",
        #     "funcion": "Team Cherry",
        #     "provider": "Team Cherry",
        #     "slug": "undefined",
        #     "Series": "Hollow Knight Chapter One Quirrel",
        #     "Volume": "2017",
        #     "Publisher": "Team Cherry",
        # }
        for manga in mangas:
            if not os.path.exists(manga["destino"]):
                os.makedirs(manga["destino"])
            if manga["slug"] != "undefined" and not os.path.exists(
                manga["destino"] + "/poster.jpg"
            ):
                if manga["Publisher"] in ["DC Comics", "Marvel"]:
                    posterc(manga)
                else:
                    posterm(manga)
            file2 = manga["Series"]
            path3 = manga[
                "origen"
            ]  # "/media/cristian/Datos/Comics/Tachiyomi/Manually/Hollow Knight"
            files2 = os.listdir(path3)
            files2.sort()
            for file3 in files2:
                path4 = f"{path3}/{file3}"
                organizer([file2, file3], manga, path4, mensaj, mensaj2, history, secrets)
            try:
                shutil.rmtree(path3)
            except OSError:
                print("Error while deleting directory")

        with open("/opt/tachiyomimangaexporter/history.json", "w") as outfile:
            json.dump(history, outfile)
        mensaj2.append(
            str(
                requests.post(
                    "https://komga.loyhouse.net/api/v1/libraries/02G13VGFYC532/scan",
                    data={"accept": "*/*"},
                    auth=HTTPBasicAuth(secrets["komgauser"], secrets["komgapass"]),
                )
            )
        )
        send(mensaj, mensaj2)
        os.remove(manually)


if __name__ == "__main__":
    main()
