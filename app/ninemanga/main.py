from ninemanga import loader, newmangas


def main():
    loader.init()
    loader.mensaj.append("Mangas nuevos de Ninemanga\n\n")
    newmangas.main()
    loader.save()
