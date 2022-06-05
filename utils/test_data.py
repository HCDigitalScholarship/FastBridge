# Works in FastBridgeApp dir, here for keeping TODO use importlib to load as modules 
from pathlib import Path 

from data.Latin import texts as latin
from data.Greek import texts as greek

latin_textFileDict = latin.textFileDict
greek_textFileDict = greek.textFileDict

latin_files = [a.stem for a in Path('data/Latin').iterdir() if a.is_file()]
greek_files = [a.stem for a in Path('data/Greek').iterdir() if a.is_file()]

def textFileDict_matches_files(textFileDict:dict, files:list):
    nomatch = []
    slugs = [slug for text, slug in textFileDict.items()]
    for file in files: 
        if file not in slugs:
            print(f'{file} not in textFileDict')
            nomatch.append(file)
    return nomatch

def all_files_in_texts(texts:dict, textFileDict:dict, files:list):
    missingFileDict = []
    missingtexts = []
    for file in files: 
        title = [text for text, slug in textFileDict.items() if slug == file]
        if not title:
            missingFileDict.append(file)
        else:
            if not title[0] in texts.keys():
                missingtexts.append(file)
    return missingFileDict, missingtexts

if __name__ == '__main__':
textFileDict_matches_files(latin_textFileDict, latin_files)
textFileDict_matches_files(greek_textFileDict, greek_files)
all_files_in_texts(latin.texts, latin_textFileDict, latin_files)
all_files_in_texts(greek.texts, greek_textFileDict, greek_files)
