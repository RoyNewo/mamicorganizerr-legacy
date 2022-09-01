from getcomicsinfo import loader, manuallyissue, scanweb, manuallyissuefolder, newreleasedcomic, weeklypack

def main():
    loader.init()
    loader.mensaj.append("Comics nuevos de getcomicsinfo\n\n")
    # manuallyissuefolder.main()
    newreleasedcomic.main()
    weeklypack.main()
    # manuallyissue.main()
    # scanweb.main()
    loader.save()
    