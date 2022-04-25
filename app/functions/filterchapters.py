from icecream import ic
def filterchapter(webtitle, dic):
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
    ic(webtitle)
    ic(cadena)
    # Vamos a comprobar primero si aparece las palabras clave donde el capitulo esta detras
    # Un bucle con enmuerate para tener indice y el valor de la lista
    # La lista es el string separado por espacios por lo que cada indice es una palabra
    for indx , palabra in enumerate(cadena.split()):
        if palabra in tags:
            numero = cadena.split()[indx + 1]
    if not numero:
        sintitulo = webtitle.lower().replace(dic['Series'].lower(), "")
        if 'keyword' in dic:
            for numero in enumerate(dic['keyword']):
                ic(numero)
                sintitulo = sintitulo.replace(dic['keyword'][numero[0]].lower(), "")
        ic(dic['Series'].lower())
        ic(sintitulo)
        ic(sintitulo.split()[0])
        if (
            sintitulo.split()[0].isnumeric()
            or not sintitulo.split()[0].isnumeric()
            and "." in sintitulo.split()[0]
        ):
            numero = sintitulo.split()[0]
        else:
            numero = f'{sintitulo.split()[0]} , {webtitle}'

    return numero