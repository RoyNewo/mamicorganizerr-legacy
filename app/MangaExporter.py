# -*- coding: utf-8 -*-
import json
import os
import shutil
import time
from subprocess import Popen, PIPE, call
import telegram
import sys
import traceback
import functions.organizer as organizar
import functions.mangaplus as MangaPlus
import functions.explosm as explosm
import ninemanga.main
import requests
from requests.auth import HTTPBasicAuth
from discord import Webhook, RequestsWebhookAdapter
from icecream import ic
from functions.organizer import sendmsgdiscord, sendmsgtelegram
import check_ips_and_ports
from getmac import get_mac_address



def my_exception_hook(type, value, tb):
    with open("/opt/tachiyomimangaexporter/secrets.json") as json_file2:
        secretos = json.load(json_file2)
    traceback_details = "\n".join(traceback.extract_tb(tb).format())
    error_msg = (
        "Mangaexporter: An exception has been raised outside of a try/except!!!\n"
        f"Type: {type}\n"
        f"Value: {value}\n"
        f"Traceback: {traceback_details}"
    )
    print(error_msg)

    n = 4000
    for i in range(0, len(error_msg), n):
        bot = telegram.Bot(token=secretos["token"])
        bot.sendMessage(chat_id=secretos["chatid"], text=error_msg[i : i + n])
        time.sleep(2)
    n = 1900
    for i in range(0, len(error_msg), n):
        webhook = Webhook.from_url(
            secretos["disdcordwebhookfallo"],
            adapter=RequestsWebhookAdapter(),
        )
        webhook.send(error_msg[i : i + n])


# def conexion(secret):
#     nmap = nmap3.Nmap()
#     results = nmap.scan_top_ports("192.168.1.0/24", args="-sP -n")
#     check_ips_and_ports.check_subnet_for_open_port("192.168.1", 5555)
#     conect = ""
#     # print(json.dumps(results))
#     for key in results:
#         # print(key)
#         if (
#             "macaddress" in results[key]
#             and results[key]["macaddress"] != None
#             and "addr" in results[key]["macaddress"]
#             and results[key]["macaddress"]["addr"] == "B8:27:EB:95:9F:BD"
#         ):
#             # print(key)
#             if key != secret["ip"]:
#                 secret["ip"] = key
#                 with open("/opt/tachiyomimangaexporter/secrets.json", "w") as outfile:
#                     json.dump(secret, outfile)
#             conect = key
#     return conect if conect != "" else None

def conexion(secrets):
    if address := check_ips_and_ports.check_subnet_for_open_port(secrets["rango"], int(secrets["puerto"])):
        ic(address)
        for direccion in address:
            ip_mac = get_mac_address(ip=direccion)
            if ip_mac == secrets["mac"]:
                if direccion != secrets["ip"]:
                    secrets["ip"] = direccion
                    with open("/opt/tachiyomimangaexporter/secrets.json", "w") as outfile:
                        json.dump(secrets, outfile)
                return direccion


def main():
    sys.excepthook = my_exception_hook
    organizar.komgabookid()
    mensaj2 = []
    excludes = [
        "/media/cristian/Datos/Comics/Tachiyomi/automatic",
        "/media/cristian/Datos/Comics/Tachiyomi/Manually",
        "/media/cristian/Datos/Comics/Tachiyomi/Updates",
        "/media/cristian/Datos/Comics/Tachiyomi/backup",
    ]

    with open("/opt/tachiyomimangaexporter/mangas.json") as json_file:
        mangas = json.load(json_file)
    with open("/opt/tachiyomimangaexporter/secrets.json") as json_file2:
        secrets = json.load(json_file2)
    # organizar.issueupdate(secrets, mangas)
    MangaPlus.mangaplusmain()
    ninemanga.main.main()
    explosm.cyanide("/media/cristian/Datos/Comics/Tachiyomi/Cyanide & Happiness (EN)/C&H 2022")
    ic("conexion")
    with open("/opt/tachiyomimangaexporter/history.json") as json_file3:
        history = json.load(json_file3)
    conect = f"adb connect {conexion(secrets)}:{str(secrets['puerto'])}"
    os.system(conect)
    time.sleep(5)
    os.system("adb pull /storage/emulated/0/Tachiyomi /media/cristian/Datos/Comics")
    mensaj = ["Revision de Mangas de Tachiyomi\n\n"]
    path = "/media/cristian/Datos/Comics/Tachiyomi"
    dirs = os.listdir(path)
    dirs.sort()
    for file1 in dirs:
        path2 = f"{path}/{file1}"
        if path2 not in excludes and os.path.isdir(path2):
            files = os.listdir(path2)
            for file2 in files:
                path3 = f"{path2}/{file2}"
                # print(path3)
                if path3 in mangas:
                    if path3 not in excludes and os.path.isdir(path3):
                        files2 = os.listdir(path3)
                        for file3 in files2:
                            path4 = f"{path3}/{file3}"
                            organizar.organizer(
                                [file2, file3],
                                mangas[path3],
                                path4,
                                mensaj,
                                mensaj2,
                                history,
                                secrets
                            )
                            with open("/opt/tachiyomimangaexporter/history.json", "w") as outfile:
                                json.dump(history, outfile)
                            mensaj = []
                            mensaj2 = []
                else:
                    shutil.move(
                        path3, "/media/cristian/Datos/Comics/Tachiyomi/Manually"
                    )
                    mensaj2.append(
                        path3
                        + " El Manga no existe en la biblioteca y se ha movido a la carpeta Manually \n\n"
                    )
                    sendmsgtelegram.sendmsg(secrets["token"], secrets["chatid"], mensaj2)
                    sendmsgdiscord.sendmsg(secrets["disdcordwebhookfallo"], mensaj2)
                    mensaj2 = []
    os.system(
        'adb shell "find /storage/emulated/0/Tachiyomi/ -type d -mindepth 3 -exec rm -rf "{}" \;"'
    )

    mensaj.append('scan')
    organizar.scankomgalibrary(
        mensaj, mensaj2, secrets["komgauser"], secrets["komgapass"], secrets
    )
    # organizar.send(mensaj, mensaj2)


if __name__ == "__main__":
    main()
