from hashlib import new
import json
from icecream import ic
def main():
    configs = "/opt/tachiyomimangaexporter/"

    with open(f'{configs}mangas.json') as mangas_file:
        mangas = json.load(mangas_file)

    lista = [[mangas[manga]['Series'], manga] for manga in mangas]
    # ic(sorted(lista, key=lambda x: x[0]))
    newmangas = {key[1]: mangas[key[1]] for key in sorted(lista, key=lambda x: x[0])}

    with open(f'{configs}newmangas.json', "w") as newmangas_file:
        json.dump(newmangas, newmangas_file)

if __name__ == "__main__":
    main()