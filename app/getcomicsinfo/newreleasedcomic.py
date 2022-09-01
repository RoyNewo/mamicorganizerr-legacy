import requests
from requests.auth import HTTPBasicAuth
import getcomicsinfo.loader as loader
import itertools
from icecream import ic

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
    query = f'https://komga.loyhouse.net/api/v1/series/{dic["komga_serie_id"]}/books?sort=name%2Cdesc'
    reponse = requests.get(
        query,
        data={"accept": "*/*"},
        auth=HTTPBasicAuth(
            loader.secrets["komgauser"], loader.secrets["komgapass"]),
    )
    
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

def get_last_issues(dic):
    komganumber = from_komga(dic)
    issues, comicvinenumber, series = from_comicvine(dic)
    pending_issues = None
    issues = check_specials(issues)
    if comicvinenumber["id"] in loader.annual_issues:
        comicvinenumber["issue_number"] = loader.annual_issues[comicvinenumber["id"]]["newnumber"]
    ic(dic["Series"], komganumber, comicvinenumber["issue_number"])
    if int(komganumber) != comicvinenumber["issue_number"]:
        pending_issues = [[issue, series] for issue in issues if float(issue["issue_number"]) > float(komganumber)]
    ic(pending_issues)
    return pending_issues or False


    


def filter_comics():
    return [key for key in loader.mangas if loader.mangas[key]["slug"][:4] == '4050']


def main():
    comics = filter_comics()
    for comic in comics:
        if pending_issues := get_last_issues(loader.mangas[comic]):
            for idx, pending_issue in enumerate(pending_issues):
                ic(idx)
                loader.pendingissues.append([comic, pending_issue[0]["id"]], pending_issue[1], '{:0>3}'.format(pending_issue[0]['issue_number']))
                if idx == 0:
                    loader.apobj.notify(
                        body=f"{pending_issue[1]}: {'{:0>4}'.format(pending_issue[0]['issue_number'])} - {pending_issue[0]['name']}",
                        title='Pending issues from comics found:',
                        tag='ok',
                    )
                else:
                    loader.apobj.notify(
                        body=f"{pending_issue[1]}: {'{:0>4}'.format(pending_issue[0]['issue_number'])} - {pending_issue[0]['name']}",
                        title='',
                        tag='ok',
                    )
    ic(loader.annual_issues)




if __name__ == '__main__':
    main()