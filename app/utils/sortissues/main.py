from utils.sortissues import loader, comicvinesort


def main():
    loader.init()
    comicvinesort.main()
    loader.save()
