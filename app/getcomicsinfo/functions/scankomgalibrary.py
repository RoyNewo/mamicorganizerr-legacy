import requests
from requests.auth import HTTPBasicAuth
from functions import sendmsgdiscord, sendmsgtelegram



def scankomgalibrary(mensaj, mensaj2, user, password, secrets):
    print(mensaj, mensaj2)
    print("paso por aqui")
    response = requests.post(
        "https://komga.loyhouse.net/api/v1/libraries/02G13VGFYC532/scan",
        data={"accept": "*/*"},
        auth=HTTPBasicAuth(user, password),
    )
    if response.status_code != 202:
        mensaj2.append(str(response))
        sendmsgtelegram.sendmsg(secrets["token"], secrets["chatid"], mensaj2)
        sendmsgdiscord.sendmsg(secrets["disdcordwebhookfallo"], mensaj2)