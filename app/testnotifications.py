import apprise
import time

def main():
    apobj = apprise.Apprise()

    # Create an Config instance
    config = apprise.AppriseConfig()

    # Add a configuration source:
    config.add('/opt/tachiyomimangaexporter/apprise.yml')

    # Make sure to add our config into our apprise object
    apobj.add(config)
    # portrait = f"{portrait}&random=64"
    apobj.notify(
        body="nuevomanga",
        title="Se ha detectado un nuevo manga en la aplicacione MangaPlus",
        # attach=portrait,
        tag='ok',
    )
    time.sleep(2)



if __name__ == "__main__":
    main()
