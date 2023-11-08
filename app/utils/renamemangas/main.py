from utils.renamemangas import loader, renamemanga


def main():
    loader.init()
    renamemanga.main()
    loader.save()
