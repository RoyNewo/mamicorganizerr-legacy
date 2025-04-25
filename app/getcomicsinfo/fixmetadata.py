import requests
# from requests.auth import HTTPBasicAuth
import itertools
import getcomicsinfo.loader as loader
import getcomicsinfo.sortissue_fixmetadata as sortissue_fixmetadata
from getcomicsinfo.functions import scankomgalibrary
import glob
# import re
import logging
from sys import stdout

logger = logging.getLogger(__name__)
fmt = "%(filename)-20s:%(lineno)-4d %(asctime)s %(message)s"
logging.basicConfig(
    level=logging.INFO, format=fmt, handlers=[logging.StreamHandler(stdout)]
)


def check_specials(issues):
    specials = ['Annual', 'HU', 'LR', 'BEY']

    for issue, special in itertools.product(issues, specials):
        if special in str(issue["issue_number"]):
            for idx, thisissue in enumerate(issues):
                if thisissue['issue_number'] == issue['issue_number']:
                    newnumber = float(f"{issues[idx - 1]['issue_number']}.5")
                    loader.annual_issues[issue['id']] = {"newnumber": '{:0>3}'.format(newnumber), "oldnumber": issue['issue_number']}

                    issues[idx]['issue_number'] = newnumber
    return issues


def datafromcomicvine(slug):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36"
    }
    url = f"https://comicvine.gamespot.com/api/volume/{slug}/?api_key=dcb22bb374f04e7217eaca81f2fcfffbe5062e42&format=json"
    responsevolume = requests.get(url, headers=headers)
    datavolume = responsevolume.json()
    return datavolume["results"]["issues"]


def file_issue_number(file):
    issue_number = file.split('#')[-1].split('.')[0]
    return f"{issue_number:0>4}"


def main():
    comiclocaldb = {
        "destino": "/home/data/Comics/Buffer/The Amazing Spider-Man (2022)",
        "slug": "4050-142577"
    }

    issues = datafromcomicvine(comiclocaldb["slug"])
    issues = check_specials(issues)

    for issue in issues:
        files = glob.glob(
            f"{comiclocaldb['destino']}/**/*.[cC][bB][zZrR]",
            recursive=True,
        )
        logger.info(issue)
        fixblanks = issue['issue_number'].replace(' ', '')
        issue_number = f"{fixblanks:0>4}"
        for file in files:
            issue_number_file = file_issue_number(file)
            if issue_number_file == issue_number:
                issuedata = {
                    "path": file,
                    "dic": comiclocaldb,
                    "id": issue["id"]
                }
                sortissue_fixmetadata.main(issuedata)

    scankomgalibrary.scankomgalibrary(
        loader.mensaj,
        loader.mensaj2,
        loader.secrets["komgauser"],
        loader.secrets["komgapass"],
        loader.secrets,
    )


if __name__ == "__main__":
    main()
