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


def main():
    


if __name__ == "__main__":
    main()
