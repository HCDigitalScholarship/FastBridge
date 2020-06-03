import csv
title = "Ovid, Metamorphoses" #get from input, the text's human title
filename = title.lower().replace(" ", "_").replace(",","") #get from input, what to save it as, should be the human title but lowercase and with _ instead of space, and remove commas.
section_level = 2 #GET FROM INPUT
csv_name = "Ovid-Met-Lemmatized-All" #get from input
language = "Latin" #get from input
section_words = {"start" : -1}
the_text = []
section_list ={} #sections as a linked list, so that we can find the previous one really quickly
if section_level == 1:
    section_list ={"1": "start"}
elif section_level == 2:
    section_list ={"1.1": "start"}
elif section_level == 3:
    section_list ={"1.1.1": "start"}

with open(csv_name + '.csv', newline='') as csvfile:
    reader = csv.reader(csvfile, delimiter=',', quotechar='"')
    #rows are expected to come in as :CHECK	TITLE	TEXT FORM	LOCATION	RUNNING COUNT	DISPLAYLEMMA	SHORTDEF	PROBLEM. However, the first and last of these (CHECK and PROBLEM) can probably be removed. DISPLAYLEMMA should probably also only come from the dictionary.
    for row in reader:
        #print(row)
        the_text.append((row[1], row[7], (int(row[5])-1))) #add the lemma, definition, array index triple to that list
        section = row[3].replace("_", ".") #change _ to . in sections, because excell messes up if this is done there
        section_words.update({section : (int(row[5])-1)} )
        #running count is number of words starting at 1, but we need them starting at 1. section_words will store the END of sections

    unique_sections = list(section_words.keys()) #hopefully they are still in order, but there is no guarntee because dictionaries are not ordered.
    for i in range(len(unique_sections) - 1):
        section_list[unique_sections[i+ 1]] =  unique_sections[i]


code = f'import text\nsection_words = {section_words}\nthe_text =  {the_text}\nsection_list ={section_list}\ntitle = "{title}"\nsection_level =  {section_level}\nlanguage = "{language}"\nbook = text.Text(title, section_words, the_text, section_list, section_level, language)'
print(code)
with open(filename + '.py', 'w') as f:
	print(code, file=f)
