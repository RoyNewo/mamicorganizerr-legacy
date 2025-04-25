from icecream import ic
from time import sleep
import requests
import json
from bs4 import BeautifulSoup

headers = {
    'Content-Type': 'application/json',
}

def flaresolverrresponse(data):
    statusok = False
    contador = 0
    while not statusok and contador < 10:
        ic("Intentando conexion")
        r = requests.post('http://royflix.net:8191/v1', headers=headers, data=data)
        response = json.loads(r.text)
        ic(response)
        if response["status"] == "ok":
            statusok = True
        else:
            contador += 1
            ic(f"Intento fallido, intento número {contador}")
            sleep(60)
    return statusok, response

def main():
    webpages = [
       'https://getcomics.info/tag/dc-week/',
       'https://getcomics.info/tag/marvel-now/'
    ]
    createsession = '{ "cmd": "sessions.create", "session": "getcomicinfo" }'

    r =requests.post('http://royflix.net:8191/v1', headers=headers, data=createsession)

    for web in webpages:
        data = '{ "cmd": "request.get", "url": "' + web + '", "session": "getcomicinfo" }'
        statusok, response = flaresolverrresponse(data)
        if not statusok:
            destroysession = '{ "cmd": "sessions.destroy", "session": "getcomicinfo"}'

            requests.post('http://royflix.net:8191/v1', headers=headers, data=destroysession)
        else:
            soup = BeautifulSoup(response["solution"]["response"], 'lxml')
            nextpage = soup.find('a', class_='pagination-button pagination-older').contents[0]
            ic(nextpage)