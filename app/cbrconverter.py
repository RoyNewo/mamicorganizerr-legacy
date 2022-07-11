import patoolib
import os
from os.path import basename
import re
import json
import shutil
import xml.etree.cElementTree as ET
import glob
from zipfile import ZipFile
from modifieddate import datemodified
from icecream import ic

def cbzgenerator(namefile, origen):
    logfile = f'{origen}/cbrconverter.log'
    parents, filename = os.path.split(namefile)
    temporal = f'{parents}/temporal'
    try:
        os.mkdir(temporal)
    except OSError:
        print(f"Creation of the directory {temporal} failed")
    print(namefile)
    try:
        patoolib.extract_archive(namefile, outdir=temporal)
    except:
        with open(logfile, "a") as f:
            f.write(f"Error descomprimiendo: {namefile}" + '\n')
        try:
            shutil.rmtree(temporal)
        except OSError:
            print('Error while deleting directory')
    os.rename(namefile, f"{namefile}.extraido")
    archivos = glob.glob(f'{temporal}/**/*.*', recursive=True)
    archivos.sort()

    filename2, file_extension = os.path.splitext(filename)
    cbz = f'{parents}/{filename2}.cbz.new'
    zipobje = ZipFile(cbz, 'w')
    for archivos2 in archivos:
        datemodified(archivos2)
        ruta, nombrearchivo = os.path.split(archivos2)
        zipobje.write(archivos2, basename(nombrearchivo))
    zipobje.close()
    try:
        shutil.rmtree(temporal)
    except:
        print('Error while deleting directory')

def main():
    ic("eso")
    path = "/media/cristian/Datos/Comics/Buffer/msmarvel"
    # path = "/media/cristian/Datos/Comics/Buffer/cbr"

    files = glob.glob(f'{path}/**/*.[cC][bB][rR]', recursive=True)
    files2 = glob.glob(f'{path}/**/*.[cC][bB][zZ]', recursive=True)
    ic(files)
    # print(files)
    # print(files2)
    # for ficheros in files:
    #     parents, filename = os.path.split(ficheros)
    for ficheros in files:
        cbzgenerator(ficheros,path)
    for ficheros2 in files2:
        cbzgenerator(ficheros2,path)

if __name__ == "__main__":
    main()
