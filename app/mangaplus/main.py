from mangaplus import loader, newmangas


def main():
    loader.init()
    newmangas.main()
    loader.save()
