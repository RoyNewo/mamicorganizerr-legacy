from getcomicsinfo import loader, manuallyissue, scanweb, manuallyissuefolder, newreleasedcomic, weeklypack, fixmetadata


def main():
    loader.init()
    loader.mensaj.append("Comics nuevos de getcomicsinfo\n\n")
    # newreleasedcomic.main()
    # fixmetadata.main()
    # weeklypack.main()
    # manuallyissue.main()
    # manuallyissuefolder.main()
    scanweb.main()
    loader.save()
    