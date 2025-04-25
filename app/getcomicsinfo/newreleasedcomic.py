import requests
from requests.auth import HTTPBasicAuth
import getcomicsinfo.loader as loader
import itertools
from icecream import ic
import logging
from sys import stdout

logger = logging.getLogger(__name__)
fmt = f"%(filename)-20s:%(lineno)-4d %(asctime)s %(message)s"
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


def from_komga(dic):
    query = f'https://komga.royflix.net/api/v1/series/{dic["komga_serie_id"]}/books?sort=name%2Cdesc'
    reponse = requests.get(
        query,
        data={"accept": "*/*"},
        auth=HTTPBasicAuth(
            loader.secrets["komgauser"], loader.secrets["komgapass"]),
    )
    logger.info(reponse.json()["content"][0]["name"])

    return reponse.json()["content"][0]["name"].split("#")[1].lstrip("0")


def from_comicvine(dic):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36"
    }
    url = f"https://comicvine.gamespot.com/api/volume/{dic['slug']}/?api_key=dcb22bb374f04e7217eaca81f2fcfffbe5062e42&format=json"
    responsevolume = requests.get(url, headers=headers)
    datavolume = responsevolume.json()
    issues = datavolume["results"]["issues"]
    lastissue = datavolume["results"]["last_issue"]
    series = datavolume["results"]["name"].replace(":", " -")
    return issues, lastissue, series


def get_last_issues(dic, nuevo):
    if nuevo:
        komganumber = from_komga(dic)
    else:
        komganumber = 0
    issues, comicvinenumber, series = from_comicvine(dic)
    pending_issues = None
    issues = check_specials(issues)
    if comicvinenumber["id"] in loader.annual_issues:
        comicvinenumber["issue_number"] = loader.annual_issues[comicvinenumber["id"]]["newnumber"]
    logger.info('Serie: ' + dic["Series"])
    logger.info('Issue en komga: ' + str(komganumber))
    logger.info('Issue en Comicvine: ' + comicvinenumber["issue_number"])
    if float(komganumber) != comicvinenumber["issue_number"]:
        pending_issues = [[issue, series] for issue in issues if float(issue["issue_number"]) > float(komganumber)]
    logger.info(pending_issues)
    return pending_issues or False


def filter_comics():
    comics = []
    for key in loader.mangas:
        if loader.mangas[key]["slug"][:4] == '4050':
            if loader.mangas[key]["komga_serie_id"] == '':
                comics.append([key, False])
            else:
                comics.append([key, True])

    return comics


def send_notification(title, body, tag):
    loader.apobj.notify(
        body=body,
        title=title,
        tag=tag,
    )


def main():
    # Get a list of comics to check for pending issues
    comics = filter_comics()

    # Check each comic for pending issues
    for comic_key, has_komga_id in comics:
        # Get a list of pending issues for the current comic
        logger.info('Comic: ' + comic_key)
        if pending_issues := get_last_issues(loader.mangas[comic_key], has_komga_id):
            # Add each pending issue to the list of pending issues
            for issue_index, issue_info in enumerate(pending_issues):
                logger.debug("Issue RAW: " + issue_info[0]['issue_number'])
                logger.debug("Issue Modificado: " + f"{issue_info[0]['issue_number']:0>3}")
                issue_number = issue_info[0]['issue_number'].replace(' ', '')
                logger.debug("Issue sin espacios: " + issue_number)
                logger.debug("Issue sin espacios modificado: " + f"{issue_number:0>3}")
                loader.pendingissues.append([comic_key, issue_info[0]["id"], issue_info[1], f"{issue_number:0>3}"])
                # Send a notification for the first pending issue, but not for subsequent ones
                if issue_index == 0:
                    send_notification(
                        title='Pending issues from comics found:',
                        body=f"{issue_info[1]}: {issue_info[0]['issue_number']:0>4} - {issue_info[0]['name']}",
                        tag='ok',
                    )
                else:
                    send_notification(
                        title='',
                        body=f"{issue_info[1]}: {issue_info[0]['issue_number']:0>4} - {issue_info[0]['name']}",
                        tag='ok',
                    )

    logger.debug(loader.annual_issues)
    logger.debug(loader.pendingissues)


if __name__ == '__main__':
    main()
