from mangaplus import loader, newmangas,addnewmangas


def main():
    loader.init()
    # newmangas.main()
    addnewmangas.main()
    loader.save()
