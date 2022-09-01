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


def prowlar():
    response = requests.get('https://prowlarr.loyhouse.net/api/v1/search?query=%22Weekly%20Pack%22&indexerIds=18&categories=7030&type=search', headers={
                            "x-api-key": loader.secrets["prowlarrapi"]}, params={"query": "%22Weekly%20Pack%22", "indexerIds": "18", "categories": "7030", "type": "search"})

    if response.status_code == 200:
        return [[torrent['title'], torrent['guid']] for torrent in response.json() if torrent['title'] not in loader.torrentlist]


def deluge(pendingtorrents):
    ses = requests.Session()
    header = {"Content-Type": "application/json", "Accept": "application/json"}
    ses.headers = header
    url = "https://deluge.loyhouse.net/json"
    ses.post(url, headers=header, data=json.dumps(
        {"id": 1, "method": "auth.login", "params": [loader.secrets["delugepass"]]}))

    torrentsid = []
    for torrent in pendingtorrents:
        response = ses.post(url, headers=header, data=json.dumps(
            {"id": 1, "method": "webapi.add_torrent", "params": [torrent[1], {}]}))

        loader.apobj.notify(
            body=f"{torrent[0]}", title='Pending torrent added:', tag='ok')

        torrentsid.append([torrent[0], response.json()["result"]])
    ic(torrentsid)
    alltrue = False
    start = time.time()
    complete = []
    while not alltrue:
        status = ses.post(url, headers=header, data=json.dumps(
            {"id": 1, "method": "core.get_torrents_status", "params": [[], ["is_finished", "name", "hash"]]}))

        for torrent in torrentsid:
            if status.json()['result'][torrent[1]]["is_finished"] and torrent[1] not in complete:
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
                title='Deluge timed out:',
                tag='error',
            )
        else:
            for torrent in reversed(pendingtorrents):
                loader.torrentlist.insert(0, torrent[0])
                # revisar carpeta donde se descargan los comics y buscar lo que nos debemos haber traido de new releases tener cuido con amaizing spiderman que nos va a dar algun calentamiento de cabeza
                if os.path.exists(f'{loader.downloadfolder}{torrent[0]}'):
                    files = glob.glob(
                        f"{loader.downloadfolder}{torrent[0]}/**/*.[cC][bB][zZrR]", recursive=True)
                    for issue in loader.pendingissues:
                        if issue[2] in loader.annual_issues:
                            name = f"{issue[3]} {loader.annual_issues[issue[3]]['oldnumber']}"
                        else:
                            name = f"{issue[3]} {issue[4]}"
                        for file in files:
                            if name in file:
                                if issue[2] in loader.annual_issues:
                                    name = f"{issue[3]} #{loader.annual_issues[issue[3]]['newnumber']}"
                                else:
                                    name = f"{issue[3]} #{issue[4]}"
                                issuedata = {
                                    "name": name,
                                    "path": file,
                                    "dic": issue[0],
                                    "id": issue[2]
                                }
                                sortissue.main(issuedata)
                                break

                try:
                    shutil.rmtree(f'{loader.downloadfolder}{torrent[0]}')
                except Exception:
                    ic("Error while deleting directory")

    scankomgalibrary.scankomgalibrary(loader.mensaj, loader.mensaj2,
                                      loader.secrets["komgauser"], loader.secrets["komgapass"], loader.secrets)


if __name__ == "__main__":
    main()
