from mangaplus import loader, newmangas,addnewmangas, posterupdate
from icecream import ic

def main():
    loader.init()
    # newmangas.main()
    addnewmangas.main()
    loader.save()
    posterupdate.main()
    loader.save()
