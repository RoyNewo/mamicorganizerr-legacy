import requests
from requests.auth import HTTPBasicAuth
from functions import sendmsg



def scankomgalibrary(mensaj, mensaj2, user, password, secrets):
    print(mensaj, mensaj2)
    print("paso por aqui")
    response = requests.post(
        "https://komga.royflix.net/api/v1/libraries/02G13VGFYC532/scan",
        data={"accept": "*/*"},
        auth=HTTPBasicAuth(user, password),
    )
    if response.status_code != 202:
        mensaj2.append(str(response))
        sendmsg.sendnewmsg('fallo', mensaj2, 'Fallo Scaneo Komga')
        # sendmsgtelegram.sendmsg(secrets["token"], secrets["chatid"], mensaj2)
        # sendmsgdiscord.sendmsg(secrets["disdcordwebhookfallo"], mensaj2)