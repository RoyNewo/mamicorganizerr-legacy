from icecream import ic
from functions import organizer

def isfloat(x):
    try:
        float(x)
    except ValueError:
        return False
    else:
        return True


def isint(x):
    try:
        a = float(x)
        b = int(a)
    except ValueError:
        return False
    else:
        return a == b

def formatnumber(numero):  # sourcery skip: remove-redundant-if
    if isint(numero) or isfloat(numero):
        if isint(numero):
            if '.' not in numero:
                return "{:0>4}".format(numero), True
            else:
                return "{:0>4}".format(str(numero).split('.')[0]), True
        elif isfloat(numero):
            separado = numero.split(".")
            if separado[1] != '0' or separado[1] != '00':
                return "{:0>4}".format(separado[0]) + '.' + separado[1], True
            else:
                return "{:0>4}".format(separado[0]), True
    return numero, False

def filterchapter(webtitle, dic):
    organizer.folderinit(dic)
    nonumber = True
    tags = [
        "ep",
        "ch",
        "chapter",
        "chapterr",
        "chap",
        "episodio",
        "capitulo",
        "num",
        "issue",
        "generations",
    ]

    numero = ""
    cadena = (
        webtitle.lower()
        .replace("ch.", "ch ")
        .replace(":", " ")
        .replace(u"núm.", "num ")
        .replace(u"ó", "o")
        .replace(u"á", "a")
        .replace(u"́é", "e")
        .replace(u"í", "i")
        .replace(u"ú", "u")
        .replace(u"ñ", "n")
        .replace(u"é", "e")
        .replace(u"“", "")
        .replace(u"”", "")
        .replace(u"«", "")
        .replace(u"»", "")
        .replace(u"ô", "o")
        .replace(u"â", "a")
        .replace(".hu", "")
        .replace(".lr", "")
        .replace("shueisha_", "")
        .replace("mangakakalot.com_", "")
        .replace("readmanganato.com_", "")
        .replace("_tmp", "tmp")
        .replace("_", " ")
        .replace("cap&iacute;tulo", "capitulo")
    )
    # ic(webtitle)
    # ic(cadena)
    # Vamos a comprobar primero si aparece las palabras clave donde el capitulo esta detras
    # Un bucle con enmuerate para tener indice y el valor de la lista
    # La lista es el string separado por espacios por lo que cada indice es una palabra
    for indx , palabra in enumerate(cadena.split()):
        if palabra in tags:
            numero = cadena.split()[indx + 1]
            break
            
    # Si no se saca un numero con las palabras clave sacamos un segundo metodo, vamos a eliminar de la cadena el titulo del manga, algunas palbras clave especiales, vamos a quitar caracteres raros del titulo 
    if not numero:
        sintitulo = webtitle.lower().replace(dic['Series'].lower(), "")
        if 'keyword' in dic:
            for numero in enumerate(dic['keyword']):
                # ic(numero)
                sintitulo = sintitulo.replace(dic['keyword'][numero[0]].lower(), "")
        # ic(dic['Series'].lower())
        # ic(sintitulo)
        # ic(sintitulo.split()[0])
        # eliminamos los capitulos que sean numero.00 como miramos lo del punto a veces salen algun falso positivo, por ello vamos a formatear y ver finalmente si es numerico o texto
        if (
            sintitulo.split()[0].isnumeric()
            or not sintitulo.split()[0].isnumeric()
            and "." in sintitulo.split()[0]
        ):
            numero, nonumber = formatnumber(sintitulo.split()[0])
        else:
            numero = f'{sintitulo.split()[0]} , {webtitle}'
            nonumber = False
    else:
        # formateamos el numero y comprobamos si es numerico o no
        numero, nonumber = formatnumber(numero)

    return numero, nonumber