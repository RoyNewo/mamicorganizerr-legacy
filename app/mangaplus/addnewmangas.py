import mangaplus.loader
from icecream import ic

nuevalista = {"new" : []}
def addmanga(key, index, mangaid):
    mangaplus.loader.mangas[key] = mangaplus.loader.newmanga["new"][index][key]
    mangaplus.loader.mapeo[mangaid] = key
    nuevalista['new'].append(mangaplus.loader.newmanga["new"][index])

def nodeletemanga(index):
    nuevalista['new'].append(mangaplus.loader.newmanga["new"][index])

def logic(key, index, series, provider, mangaid):
    spellcheck = False
    spellcheck2 = False
    ic(mangaplus.loader.newmanga["new"])
    while not spellcheck:
        answer = input(f'Do you want to add {series} - {provider}: (y)es or (n)o: ')
        if answer.lower() in ['y', 'yes']:
            spellcheck = True
            addmanga(key, index, mangaid)
        elif answer.lower() in ['n', 'no']:
            spellcheck = True
            while not spellcheck2:
                delete = input('Do you want to delete this new manga from new mangas list?: (y)es or (n)o: ')

                if delete.lower() in ['y', 'yes']:
                    spellcheck2 = True                
                elif delete.lower() in ['n', 'no']:
                    spellcheck2 = True
                    
                    nodeletemanga(index)
                else:
                    ic('The answer is invalid for the delete manga from list question, please try again')

        else:
            ic('The answer is invalid for the add manga question, please try again')

def main():
    for index, manga in enumerate(mangaplus.loader.newmanga["new"]):
        print(manga.keys())
        for key in manga.keys():
            print(manga[key]["Series"])
            series = manga[key]["Series"]
            provider = manga[key]["provider"]
            mangaid = manga[key]["mangaid"]
            logic(key, index, series, provider, mangaid)
    mangaplus.loader.newmanga = nuevalista
            



