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

# with open(configpath + "history.json") as history_file:
#     history = json.load(history_file)

with open(configpath + "secrets.json") as secrets_file:
    secrets = json.load(secrets_file)

# with open(configpath + komga) as komgabooksid_file:
#     komgabooksid = json.load(komgabooksid_file)


for manga in mangas:
    if str(mangas[manga]["destino"])[-1] != '/':
        url = urllib.parse.quote_plus(mangas[manga]["destino"].split("/")[-1])
    else:
        url = urllib.parse.quote_plus(mangas[manga]["destino"].split("/")[-2])
    ic(url)
    query = "https://komga.royflix.net/api/v1/series?search=%22" + url + "%22"
    reponse = requests.get(
                query,
                headers={"accept": "application/json"},
                auth=HTTPBasicAuth(secrets["komgauser"], secrets["komgapass"]),
            )
    ic(reponse.status_code)
    if reponse.status_code != 200:
        ic(reponse.content)
    serie = reponse.json()
    if int(serie["numberOfElements"]) == 1:
        mangas[manga]["komga_serie_id"] = serie["content"][0]["id"]
    else:
        ic(reponse.content)





# with open(configpath + komga, "w") as outfile:
#     json.dump(komgabooksid, outfile)

with open(configpath + "mangas.json", "w") as outfile:
    json.dump(mangas, outfile)