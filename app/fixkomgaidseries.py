import json
import requests
from requests.auth import HTTPBasicAuth


config = "/opt/tachiyomimangaexporter/"
allupdates = []

with open(f"{config}secrets.json") as secrets_file:
    secrets = json.load(secrets_file)

with open(f"{config}mangas.json") as mangas_file:
    mangas = json.load(mangas_file)


def clearseries():
    for manga in mangas:
        if manga not in allupdates:
            mangas[manga]["komga_serie_id"] = ""
            with open(f'{config}mangas.json', "w") as mangas_file:
                json.dump(mangas, mangas_file)


def getmanga(url):
    results = []
    url = url.replace("/comics", "")
    for manga in mangas:
        compareurl = mangas[manga]["destino"].replace("/media/cristian/Datos/Comics", "")
        if compareurl[-1] == "/":
            compareurl = compareurl[:-1]
        print(compareurl, url)
        if compareurl == url:
            print(manga)
            results.append(manga)
    return results


def getseries(series):
    for serie in series["content"]:
        print(serie["name"], serie["id"], serie["url"])
        toupdate = getmanga(serie["url"])
        for updatemanga in toupdate:
            allupdates.append(updatemanga)
            mangas[updatemanga]["komga_serie_id"] = serie["id"]
            with open(f'{config}mangas.json', "w") as mangas_file:
                json.dump(mangas, mangas_file)


def main():

    query = "https://komga.loyhouse.net/api/v1/series"
    response = requests.get(
        query,
        headers={"accept": "application/json"},
        auth=HTTPBasicAuth(secrets["komgauser"], secrets["komgapass"]),
    )
    series = response.json()
    totalpages = series["totalPages"]
    # print(json.dumps(series, indent=4, ensure_ascii=False))
    # print(series["totalPages"])
    i = 0
    for i in range(0, totalpages):
        query = f"https://komga.loyhouse.net/api/v1/series?page={i}"        
        response = requests.get(
            query,
            headers={"accept": "application/json"},
            auth=HTTPBasicAuth(secrets["komgauser"], secrets["komgapass"]),
        )
        series = response.json()
        getseries(series)
    print(allupdates)
    # clearseries()


if __name__ == "__main__":
    main()
