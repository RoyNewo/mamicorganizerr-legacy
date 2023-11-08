import utils.ordermangas.loader


def main():
    mangas = utils.ordermangas.loader.mangas
    orden = []
    newmangas = {}
    for manga in mangas:
        # print(mangas[manga]["Series"])
        orden.append([mangas[manga]["Series"], manga])
    orden.sort()
    for manga in orden:
        # print(manga)
        newmangas[manga[1]] = mangas[manga[1]]
    # for manga in newmangas:
    #     print(newmangas[manga])
    utils.ordermangas.loader.mangas = newmangas
