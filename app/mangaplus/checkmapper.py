import mangaplus.loader
from icecream import ic

def checkmapper():
    
    missing = []
    for mapeo in mangaplus.loader.mapeo:
        # ic(mapeo, mangaplus.loader.mapeo[mapeo])
        # ic(mangaplus.loader.mangas[mangaplus.loader.mapeo[mapeo]])
        if mangaplus.loader.mapeo[mapeo] not in mangaplus.loader.mangas:
            missing.append(mapeo)
    if missing:
        print(missing)
        return False
    else:
        return True