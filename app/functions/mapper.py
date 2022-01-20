import json

with open("/opt/tachiyomimangaexporter/mangas.json") as json_file:
    mangas = json.load(json_file)
lista = [
    {mangas[manga]["mangaid"]: manga} for manga in mangas if "mangaid" in mangas[manga]
]

print(json.dumps(lista, ensure_ascii=False))
