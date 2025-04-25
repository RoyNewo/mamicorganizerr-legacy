import getcomicsinfo.loader as loader
import getcomicsinfo.sortissue as sortissue
from getcomicsinfo.functions import scankomgalibrary
import requests
from icecream import ic
import json
import time
import os
import glob
import shutil
import re
import logging
from sys import stdout

logger = logging.getLogger(__name__)
fmt = f"%(filename)-20s:%(lineno)-4d %(asctime)s %(message)s"
logging.basicConfig(
    level=logging.INFO, format=fmt, handlers=[logging.StreamHandler(stdout)]
)


def prowlar():
    response = requests.get(
        "https://prowlarr.royflix.net/api/v1/search?query=%22Weekly%20Pack%22&indexerIds=18&categories=7030&type=search",
        headers={"x-api-key": loader.secrets["prowlarrapi"]},
        params={
            "query": "%22Weekly%20Pack%22",
            "indexerIds": "18",
            "categories": "7030",
            "type": "search",
        },
    )
    ic(response, response.status_code)
    if response.status_code == 200:
        if response.json() == []:
            intentos = 0
            while response.json() == []:
                response = requests.get(
                    "https://prowlarr.royflix.net/api/v1/search?query=%22Weekly%20Pack%22&indexerIds=18&categories=7030&type=search",
                    headers={"x-api-key": loader.secrets["prowlarrapi"]},
                    params={
                        "query": "%22Weekly%20Pack%22",
                        "indexerIds": "18",
                        "categories": "7030",
                        "type": "search",
                    },
                )
                intentos += 1
                ic(intentos)
            return [
                [torrent["title"], torrent["guid"]]
                for torrent in response.json()
                if torrent["title"] not in loader.torrentlist
            ]

        else:
            return [
                [torrent["title"], torrent["guid"]]
                for torrent in response.json()
                if torrent["title"] not in loader.torrentlist
            ]


def deluge(pendingtorrents):
    ses = requests.Session()
    header = {"Content-Type": "application/json", "Accept": "application/json"}
    ses.headers = header
    url = "https://deluge.royflix.net/json"
    ses.post(
        url,
        headers=header,
        data=json.dumps(
            {"id": 1, "method": "auth.login", "params": [
                loader.secrets["delugepass"]]}
        ),
    )

    torrentsid = []
    for torrent in pendingtorrents:
        response = ses.post(
            url,
            headers=header,
            data=json.dumps(
                {"id": 1, "method": "webapi.add_torrent",
                    "params": [torrent[1], {}]}
            ),
        )

        loader.apobj.notify(
            body=f"{torrent[0]}", title="Pending torrent added:", tag="ok"
        )

        torrentsid.append([torrent[0], response.json()["result"]])
    ic(torrentsid)
    alltrue = False
    start = time.time()
    complete = []
    while not alltrue:
        status = ses.post(
            url,
            headers=header,
            data=json.dumps(
                {
                    "id": 1,
                    "method": "core.get_torrents_status",
                    "params": [[], ["is_finished", "name", "hash"]],
                }
            ),
        )

        for torrent in torrentsid:
            if (
                status.json()["result"][torrent[1]]["is_finished"]
                and torrent[1] not in complete
            ):
                complete.append(torrent[1])
        end = time.time()
        if len(complete) == len(torrentsid) or end - start > 3600:
            alltrue = True
        else:
            ic(f"esperamos un poco ({end - start})")
            time.sleep(60)
    return end - start > 3600


def main():
    if loader.pendingissues:
        ic("prowlar")
        pendingtorrents = prowlar()
        if deluge(pendingtorrents):
            loader.apobj.notify(
                body="Deluge timed out",
                title="Deluge timed out:",
                tag="error",
            )
        else:
            for torrent in reversed(pendingtorrents):
                loader.torrentlist.insert(0, torrent[0])
                # revisar carpeta donde se descargan los comics y buscar lo que nos debemos haber traido de new releases tener cuido con amaizing spiderman que nos va a dar algun calentamiento de cabeza
                if os.path.exists(f"{loader.downloadfolder}{torrent[0]}"):
                    files = glob.glob(
                        f"{loader.downloadfolder}{torrent[0]}/**/*.[cC][bB][zZrR]",
                        recursive=True,
                    )
                    for issue in loader.pendingissues:
                        ic(issue)
                        # miramos si el valor de comicvine esta en los comics especiales
                        if issue[1] in loader.annual_issues:
                            name = f"{issue[2]} {loader.annual_issues[issue[3]]['oldnumber']}"
                        else:
                            name = f"{issue[2]} {issue[3]}"
                        name = re.sub(" +", " ", name)
                        names = [name]
                        if "keyword" in loader.mangas[issue[0]]:
                            oldname = issue[2]
                            for newname in loader.mangas[issue[0]]["keyword"]:
                                names.append(re.sub(oldname, newname, name))
                        ic(names)
                        for file in files:
                            for comicname in names:
                                if comicname in file:
                                    if issue[1] in loader.annual_issues:
                                        name = f"{issue[2]} #{loader.annual_issues[issue[3]]['newnumber']}"
                                    else:
                                        name = f"{issue[2]} #{issue[3]}"
                                    issuedata = {
                                        "name": name,
                                        "path": file,
                                        "dic": issue[0],
                                        "id": issue[1],
                                    }
                                    sortissue.main(issuedata)
                                    break
                            else:
                                continue
                            break

                try:
                    shutil.rmtree(f"{loader.downloadfolder}{torrent[0]}")
                except Exception:
                    ic("Error while deleting directory")

    scankomgalibrary.scankomgalibrary(
        loader.mensaj,
        loader.mensaj2,
        loader.secrets["komgauser"],
        loader.secrets["komgapass"],
        loader.secrets,
    )


if __name__ == "__main__":
    main()
