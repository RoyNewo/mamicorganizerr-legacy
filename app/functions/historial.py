import ninemanga.loader
def historial(history, issue, dic, komgabookid):
    if dic["Series"] in history:
        if issue in history[dic["Series"]]:
            if dic["provider"] == history[dic["Series"]][issue]:
                return False
            if dic["funcion"] == history[dic["Series"]][issue]:
                return False
            if issue in komgabookid[dic["Series"]]:
                history[dic["Series"]].pop(issue, None)
                return "update"
            else:
                ninemanga.loader.mensaj2.append(f"{dic['Series']} - {dic['provider']} - {issue}: Aun no esta en komgabookid y no se puede actualizar se hara en la siguiente ejecucion \n\n")
                return False
        else:
            history[dic["Series"]].update({issue: dic["provider"]})
            return True
    else:
        history[dic["Series"]] = {issue: dic["provider"]}
        return True