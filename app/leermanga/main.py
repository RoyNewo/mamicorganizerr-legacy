from leermanga import loader, newmangas, testsite


def main():
    loader.init()
    loader.mensaj.append("Mangas nuevos de Ninemanga\n\n")
    testsite.main()
    loader.save()
