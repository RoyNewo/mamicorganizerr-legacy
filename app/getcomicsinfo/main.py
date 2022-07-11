from getcomicsinfo import loader, manuallyissue, scanweb

def main():
    loader.init()
    loader.mensaj.append("Comics nuevos de getcomicsinfo\n\n")
    manuallyissue.main()
    # scanweb.main()
    loader.save()