import json
from urllib import response
from icecream import ic
import requests
from requests.auth import HTTPBasicAuth
import urllib

configpath = "/opt/tachiyomimangaexporter/"

komga = "komgabooksid.json"

with open(configpath + "mangas.json") as mangas_file:
    mangas = json.load(mangas_file)

with open(configpath + "history.json") as history_file:
    history = json.load(history_file)

with open(configpath + "secrets.json") as secrets_file:
    secrets = json.load(secrets_file)

with open(configpath + komga) as komgabooksid_file:
    komgabooksid = json.load(komgabooksid_file)


intermedia = {mangas[manga]["Series"]: manga for manga in mangas}

for serie in history:
    for capitulo in history[serie]:
        if serie not in komgabooksid:
            nombre = mangas[intermedia[serie]]["name"] + capitulo
            # ic(nombre)
            url = urllib.parse.quote_plus(nombre)
            ic(url)
            query = (
                "https://komga.loyhouse.net/api/v1/books?search=%22"
                + url
                + "%22&library_id=02G13VGFYC532"
            )
            reponse = requests.get(
                query,
                data={"accept": "*/*"},
                auth=HTTPBasicAuth(secrets["komgauser"], secrets["komgapass"]),
            )
            ic(reponse.json())
            book = reponse.json()
            komgabooksid[mangas[intermedia[serie]]["Series"]] = {
                        capitulo: book["content"][0]["id"]
                    }

        elif capitulo not in komgabooksid[serie]:
                nombre = mangas[intermedia[serie]]["name"] + capitulo
                # ic(nombre)
                url = urllib.parse.quote_plus(nombre)
                ic(url)
                query = (
                    "https://komga.loyhouse.net/api/v1/books?search=%22"
                    + url
                    + "%22&library_id=02G13VGFYC532"
                )
                reponse = requests.get(
                    query,
                    data={"accept": "*/*"},
                    auth=HTTPBasicAuth(secrets["komgauser"], secrets["komgapass"]),
                )
                ic(reponse.json())
                book = reponse.json()
                
                komgabooksid[mangas[intermedia[serie]]["Series"]].update(
                    {capitulo: book["content"][0]["id"]}
                )
                

    with open(configpath + komga, "w") as outfile:
        json.dump(komgabooksid, outfile)


with open(configpath + komga, "w") as outfile:
    json.dump(komgabooksid, outfile)
