from zipfile import ZipFile
import json
from pathlib import Path
import xmltodict
import patoolib
import os
import shutil
from icecream import ic
import glob
from os.path import basename

from functions.organizer import scankomgalibrary, send

# Ejemplo de estructura del json que pide este script
# [
#     {
#         "name": "Kono Subarashii Sekai Ni Shukufuku Wo (2014) Issue #16.00.cbz",
#         "mangasid": "/media/cristian/Datos/Comics/Tachiyomi/LectorManga (ES)/KonoSuba_ God's Blessing on this Wonderful World!",
#         "numero": "0016"
#     }
# ]

mensaj = []
mensaj2 = []
delete = "Error while deleting "
renamefile = Path("/media/cristian/Datos/Comics/Buffer/rename.json")
with open("/opt/tachiyomimangaexporter/mangas.json") as mangas_file:
    mangas = json.load(mangas_file)

with open("/opt/tachiyomimangaexporter/history.json") as history_file:
    history = json.load(history_file)

if renamefile.is_file():
    with open(renamefile) as rename_file:
        renames = json.load(rename_file)

    for files in renames:
        # mangas[files["mangasid"]]["destino"] : donde se guardan los mangas literalmente del archivo renames el equivalente a la ruta que hay mangas.json
        thisfile = Path(mangas[files["mangasid"]]["destino"] + "/" + files["name"])
        temporal = Path(mangas[files["mangasid"]]["destino"] + "/temporal")
        thisfilenumber = str(files["name"]).split("#")[1].replace(".cbz","")
        if os.path.exists(temporal):
            try:
                shutil.rmtree(temporal)
            except OSError:
                print(f"{delete}directory TEMPORAL")
        try:
            os.mkdir(temporal)
        except OSError:
            print(f"Creation of the directory {temporal} failed")

        patoolib.extract_archive(str(thisfile), outdir=str(temporal))
        comicinfo = Path(f"{str(temporal)}/ComicInfo.xml")
        with open(comicinfo, "r") as xml_obj:
            # coverting the xml data to Python dictionary
            my_dict = xmltodict.parse(xml_obj.read())
            # closing the file
        xml_obj.close()
        ic(my_dict["ComicInfo"], my_dict["ComicInfo"]["Series"])
        my_dict["ComicInfo"]["Number"] = files["numero"]
        with open(comicinfo, "w") as result_file:
            result_file.write(xmltodict.unparse(my_dict))
        archivos = glob.glob(f"{str(temporal)}/**/*.*", recursive=True)
        archivos.sort()
        newfile = Path(
            mangas[files["mangasid"]]["destino"]
            + "/"
            + mangas[files["mangasid"]]["name"]
            + files["numero"]
            + ".cbz"
        )
        if newfile.is_file():
            try:
                os.remove(str(newfile))
            except OSError:
                print(delete + str(newfile))
        zipobje = ZipFile(str(newfile), "w")
        for archivos2 in archivos:
            nombrearchivo = os.path.split(archivos2)
            zipobje.write(archivos2, basename(nombrearchivo[1]))
        zipobje.close()

        try:
            os.remove(str(thisfile))
        except OSError:
            print(delete + str(thisfile))
        if (
            str(files["numero"])
            not in history[str(mangas[files["mangasid"]]["Series"])]
        ):
            history[str(mangas[files["mangasid"]]["Series"])][str(files["numero"])] = history[str(mangas[files["mangasid"]]["Series"])][thisfilenumber]

        history[str(mangas[files["mangasid"]]["Series"])].pop(thisfilenumber)



        mensaj.append(str(files["name"]) + "se ha renombrado a " + str(mangas[files["mangasid"]]["name"]) + str(files["numero"]) + "\n\n")
    try:
        shutil.rmtree(temporal)
    except OSError:
        print(f"{delete}directory TEMPORAL")

    try:
        os.remove(str(renamefile))
    except OSError:
        print(delete + str(renamefile))

    with open("/opt/tachiyomimangaexporter/secrets.json") as secrets_file:
        secrets = json.load(secrets_file)
    with open("/opt/tachiyomimangaexporter/history.json", "w") as outfile:
        json.dump(history, outfile)
    scankomgalibrary(mensaj, mensaj2, secrets["komgauser"], secrets["komgapass"], secrets)
    send(mensaj, mensaj2)

