import json
from functions import organizer
from icecream import ic

def formatnumber(numero):
    if organizer.isint(numero) or organizer.isfloat(numero):
        if organizer.isint(numero):
            if '.' not in numero:
                return "{:0>4}".format(numero)
            else:
                return "{:0>4}".format(str(numero).split('.')[0])
        elif organizer.isfloat(numero):
            separado = numero.split(".")
            if separado[1] != '0' or separado[1] != '00':
                return "{:0>4}".format(separado[0]) + '.' + separado[1]
            else:
                return "{:0>4}".format(separado[0])
    return numero

def process(dic):
    newdic = {}
    for manga in dic:
        newdic[manga] = {}
        for issue in dic[manga]:
            nuevonumero = formatnumber(issue)
            # ic(manga, issue, nuevonumero)
            newdic[manga][nuevonumero] = dic[manga][issue]
    return newdic


def main():
    configs = "/opt/tachiyomimangaexporter/"
    with open(f'{configs}komgabooksid.json') as komgabooksid_file:
        komgabooksid = json.load(komgabooksid_file)
    with open(f'{configs}history.json') as history_file:
        history = json.load(history_file)
    
    newhistory = process(history)
    newkomgabooksid = process(komgabooksid)

    with open(f'{configs}newkomgabooksid.json', "w") as newkomgabooksid_file:
        json.dump(newkomgabooksid, newkomgabooksid_file)
    with open(f'{configs}newhistory.json', "w") as newhistory_file:
        json.dump(newhistory, newhistory_file)





if __name__ == "__main__":
    main()