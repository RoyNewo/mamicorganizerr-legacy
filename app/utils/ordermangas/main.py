from utils.ordermangas import loader, ordermanga


def main():
    loader.init()
    ordermanga.main()
    loader.save()
