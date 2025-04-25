import os
import json
import telegram
from functions import p2i


ruta = "/home/data/Downloads/Comics/Tokyo Ghoul"
with open("/opt/tachiyomimangaexporter/secrets.json") as json_file2:
    secrets = json.load(json_file2)

# print(os.listdir(ruta))
bot = telegram.Bot(token=secrets["token"])
bot.sendMessage(
    chat_id=secrets["chatid"], text="Comienza a convertir pdf a imagenes para " + ruta
)
files = []

for r, d, f in os.walk(ruta):
    for file in f:
        if ".pdf" in file or ".PDF" in file:
            files.append([os.path.join(r, file), file.split(".")[0]])

for f in files:
    print(f)
    bot.sendMessage(chat_id=secrets["chatid"], text="Convirtiendo " + str(f))
    p2i.splitpdf(f[0], ruta + "/" + f[1] + "/", f[1])

bot.sendMessage(
    chat_id=secrets["chatid"],
    text="Se ha terminado de convertir pdf a imagenes para " + ruta,
)
