import json

import icecream
from icecream import ic
import requests

with open("info.json") as json_file:
    capitulos = json.load(json_file)

hearders = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) Gecko/20100101 Firefox/75",
    "Accept-Language": "es-ES,es;q=0.9,en;q=0.8,gl;q=0.7",
}
for url in capitulos["volumes"]:
    n = requests.get(url["url"], headers=hearders)
    al = n.text
    print(al[al.find("<TITLE>") + 7 : al.find("</TITLE>")])
