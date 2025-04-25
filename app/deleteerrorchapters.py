import json
import requests
from requests.auth import HTTPBasicAuth

config = "/opt/tachiyomimangaexporter/"

with open(f"{config}secrets.json") as secrets_file:
    secrets = json.load(secrets_file)

with open(f"{config}mangas.json") as mangas_file:
    mangas = json.load(mangas_file)

with open(f'{config}history.json') as history_file:
    history = json.load(history_file)

with open(f'{config}komgabooksid.json') as komgabooksid_file:
    komgabooksid = json.load(komgabooksid_file)


def deletebook(bookid):
    query = f"https://komga.royflix.net/api/v1/books/{bookid}/file"
    response = requests.delete(
        query,
        headers={"accept": "application/json"},
        auth=HTTPBasicAuth(secrets["komgauser"], secrets["komgapass"]),
    )
    print(response)


def gethistory(seriesid, name):
    chapter = name.split("#")[-1]
    for manga in mangas:
        if not "komga_serie_id" in mangas[manga]:
            mangas[manga]["komga_serie_id"] = ""
        if mangas[manga]["komga_serie_id"] == seriesid:
            print(chapter, history[mangas[manga]["Series"]][chapter], komgabooksid[mangas[manga]["Series"]][chapter])
            del history[mangas[manga]["Series"]][chapter]
            del komgabooksid[mangas[manga]["Series"]][chapter]
            with open(f'{config}history.json', "w") as history_file:
                json.dump(history, history_file)
            with open(f'{config}komgabooksid.json', "w") as komgabooksid_file:
                json.dump(komgabooksid, komgabooksid_file)
            break


def main():
    query = "https://komga.royflix.net/api/v1/books"
    response = requests.get(
        query,
        headers={"accept": "application/json"},
        auth=HTTPBasicAuth(secrets["komgauser"], secrets["komgapass"]),
    )
    books = response.json()
    totalpages = books["totalPages"]
    i = 0
    for i in range(0, totalpages):
        query = f"https://komga.royflix.net/api/v1/books?page={i}"
        response = requests.get(
            query,
            headers={"accept": "application/json"},
            auth=HTTPBasicAuth(secrets["komgauser"], secrets["komgapass"]),
        )
        books = response.json()
        for book in books["content"]:
            if book["media"]["status"] == 'ERROR':
                print(book["id"], book["seriesId"], book["name"])
                gethistory(book["seriesId"], book["name"])
                deletebook(book["id"])


if __name__ == "__main__":
    main()
