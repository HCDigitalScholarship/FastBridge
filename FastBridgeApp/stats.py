import importlib
from math import log, sqrt
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px
from text import Text
from collections import defaultdict
import spacy# for LatinCy
import csv #for hashtable of Diderich -> lexical sophistication
import matplotlib.font_manager as fm

# Define FontProperties
prop = fm.FontProperties(family='serif', size=9)

#LatinCy
#pip install https://huggingface.co/latincy/la_core_web_trf/resolve/main/la_core_web_trf-any-py3-none-any.whl

#Seaborn Themes
#sns.set_style("darkgrid")
#sns.set_context("paper")
#sns.color_palette("dark")
title_font = {'fontname':'serif', 'size':'13', 'color':'black', 'weight':'normal',
              'verticalalignment':'bottom'} # This is for the title properties
axis_font = {'fontname':'serif', 'size':'11'} # This is for the axis labels
colorblind_palette = ['#E69F00', '#56B4E9', '#009E73', '#F0E442', '#0072B2', '#D55E00', '#CC79A7']



#sns.set_context("paper")

def get_text(form_request : str, language : str):
    """
    Imports the text that was requested. This way, we only load the texts that the user is requesting each time.
    """
    return importlib.import_module(f'data.{language}.{form_request}') #point to the data folder

def calculate_total_words(text_instance: Text):
    '''
    Calculate the total amount of words in the text given
    '''
    total_words = len(text_instance.words)
    print(f"Total number of words: {total_words}")



def calculate_total_sections(text_instance: Text):
    '''
    Calculate the number of sections in the text
    '''
    total_sections = len(text_instance.sections)
    print(f"Total sections: {total_sections}")



def calculate_avg_words_per_section(text_instance: Text):
    '''
    Calculate the avg number of words per section. Can also be words per sentence???
    '''
    total_words = len(text_instance.words)
    total_sections = len(text_instance.sections)
    avg_words_per_section = total_words / total_sections


    print(f"Average words per section: {avg_words_per_section:.2f}")











##########################################################################################

#All functions below the hashtag line can find attributes of text in specific sections

# Function to get the number of words in a text
def get_number_of_words(text_object: Text, start_section, end_section):
    '''
    Find the number of words in a predefined section of the book by subtracting the word numbers within Text.sections
    '''
    start_index = text_object.sections[start_section]
    end_index = text_object.sections[end_section]
    word_count = end_index - start_index
    if start_section == 'start' and end_section == 'end':
        word_count = text_object.words[-1][1]
    return word_count

# Function to get the size of the text's vocabulary
def get_vocabulary_size(text_object: Text, start_section, end_section):
    start_index = text_object.sections[start_section]
    end_index = text_object.sections[end_section]
    text_slice = text_object.words[start_index:end_index]

    if start_section == 'start' and end_section == 'end':
        text_slice = text_object.words

    vocabulary = set(word[0] for word in text_slice)
    return len(vocabulary)

# Function to display distribution of average word length
def plot_avg_word_length(text_object: Text, start_section, end_section):
    start_index = text_object.sections[start_section]
    end_index = text_object.sections[end_section]
    text_slice = text_object.words[start_index:end_index]

    if start_section == 'start' and end_section == 'end':
        text_slice = text_object.words

    df = pd.DataFrame(text_slice, columns=["Word", "Index", "Lemma", "Definition", "Notes", "Section", "Word Count"])
    df['Word Length'] = df['Word'].apply(len)
    avg_word_length = df.groupby('Section')['Word Length'].mean().reset_index()
    
    # determine the step size for x-axis labels
    n_sections = avg_word_length['Section'].nunique()
    step_size = max(1, n_sections // 20)  # adjust this factor to change the number of labels displayed
    
    plt.figure(figsize=(10,5))
    
    sns.set_style("ticks")
    sns.set_context("paper")
    lineplot = sns.barplot(data=avg_word_length, x='Section', y='Word Length', palette = colorblind_palette, width = 0.9)
    sns.despine()
    plt.title(f"Average Word Length per Section of {text_object.name}", **title_font)
    plt.xlabel('Section', **axis_font)
    plt.ylabel('Word length', **axis_font)
    # set x-tick labels with a step size
    for ind, label in enumerate(lineplot.get_xticklabels()):
        if ind % step_size == 0:  # only show labels for every nth section
            label.set_visible(True)
        else:
            label.set_visible(False)

    plt.xticks(rotation=90)
    # Get the current Axes instance
    ax = plt.gca()

    # set font properties to x and y tick labels
    plt.setp(ax.get_xticklabels(), fontproperties=prop)
    plt.setp(ax.get_yticklabels(), fontproperties=prop)
    plt.show()

def plot_avg_word_length2(text_object, start_section, end_section):
    start_index = text_object.sections[start_section]
    end_index = text_object.sections[end_section]
    text_slice = text_object.words[start_index:end_index]

    if start_section == 'start' and end_section == 'end':
        text_slice = text_object.words


    df = pd.DataFrame(text_slice, columns=["Word", "Index", "Lemma", "Definition", "Notes", "Section", "Word Count"])
    df['Word Length'] = df['Word'].apply(len)
    avg_word_length = df.groupby('Section')['Word Length'].mean().reset_index()

    # determine the step size for x-axis labels
    n_sections = avg_word_length['Section'].nunique()
    step_size = max(1, n_sections // 20)  # adjust this factor to change the number of labels displayed

    fig = px.bar(avg_word_length, x='Section', y='Word Length', 
                 hover_data=['Word Length'], labels={'Word Length':'Average Word Length per Section'})

    fig.update_layout(
        autosize=False,
        width=1000,
        height=500,
        xaxis_tickangle=-90,
    )

    fig.update_xaxes(
        tickmode = 'array',
        tickvals = avg_word_length['Section'][::step_size]
    )

    fig.show()


# Function to display distribution of word frequency
def plot_word_frequency(text_object: Text, start_section, end_section):
    start_index = text_object.sections[start_section]
    end_index = text_object.sections[end_section]
    text_slice = text_object.words[start_index:end_index]

    if start_section == 'start' and end_section == 'end':
        text_slice = text_object.words

    df = pd.DataFrame(text_slice, columns=["Word", "Index", "Lemma", "Definition", "Notes", "Section", "Word Count"])
    word_frequency = df['Word'].value_counts().reset_index()
    word_frequency.columns = ['Word', 'Frequency']

    sns.set_style("ticks")
    sns.set_context("paper")
    plt.figure(figsize=(10,5))
    sns.barplot(data=word_frequency[:30], x='Word', y='Frequency', palette=colorblind_palette)
    sns.despine()
    plt.title(f"Word Frequency of {text_object.name}", **title_font)
    plt.xlabel('Word', **axis_font)
    plt.ylabel('Frequency', **axis_font)
    plt.xticks(rotation=90)

    # Get the current Axes instance
    ax = plt.gca()

    # set font properties to x and y tick labels
    plt.setp(ax.get_xticklabels(), fontproperties=prop)
    plt.setp(ax.get_yticklabels(), fontproperties=prop)
    plt.show()

def find_hapax_legomena(words):
    word_frequencies = defaultdict(int)
    for word in words:
        word_frequencies[word] += 1
    return [word for word, freq in word_frequencies.items() if freq == 1]

def get_hapax_legomena(text_object: Text, start_section, end_section):
    '''
    Returns all of the words used once from each section, separated by section, it's just printing but can return in zip()
    '''
    # Get words from each section
    #sections = defaultdict(list)
    allwords = []
    start_index = text_object.sections[start_section]
    end_index = text_object.sections[end_section]
    text_slice = text_object.words[start_index:end_index]

    if start_section == 'start' and end_section == 'end':
        text_slice = text_object.words


    for word_tuple in text_slice:
        word = word_tuple[0]
        section = word_tuple[5]
        #sections[section].append(word)
        allwords.append(word)

    firstSection = text_object.words[0][5]


    # find hapax legomena per section
    '''
    for section, words in sections.items():
        hapax_legomena = find_hapax_legomena(words)
        print(f"Section {section}")
        print(f"  Hapax legomena: {hapax_legomena}")'''
    hapax_legomena = find_hapax_legomena(allwords)
    return hapax_legomena


def get_lexical_density(text_object: Text, start_section, end_section):
    nlp = spacy.load("la_core_web_trf")
    start_index = text_object.sections[start_section]
    end_index = text_object.sections[end_section]
    text_slice = text_object.words[start_index:end_index]

    if start_section == 'start' and end_section == 'end':
        text_slice = text_object.words

    #FINDING LEXICAL WORDS
    spacyString = ""

    #adding all words into big string for LatinCy
    for word_tuple in text_slice:
        word = word_tuple[0]
        if len(spacyString) == 0:
            spacyString = word
        else:
            spacyString += f" {word}"
    
    doc = nlp(spacyString)
    
    lexicalSum = 0
    lexicalCategories = ['NOUN', 'ADV', 'PROPN', 'ADJ', 'VERB']
    for token in doc:
        if token.pos_ in lexicalCategories:
            lexicalSum += 1

    #FINDING TOTAL WORDS IN SECTION
    total_words = get_number_of_words(text_object,start_section, end_section)

    lexical_density = lexicalSum/total_words

    return lexical_density

def create_hashtable_from_csv(file_path):
    hashtable = {}
    with open(file_path, 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            hashtable[row['TITLE']] = {'LOCATION': row['LOCATION'], 'SECTION': row['SECTION'], 
                                       'RUNNINGCOUNT': row['RUNNINGCOUNT'], 'TEXT': row['TEXT']}
    return hashtable


def get_lexical_sophistication(text_object: Text, start_section, end_section):
    #import os
    #print(os.getcwd())

    start_index = text_object.sections[start_section]
    end_index = text_object.sections[end_section]
    text_slice = text_object.words[start_index:end_index]

    if start_section == 'start' and end_section == 'end':
        text_slice = text_object.words

    hashTable = create_hashtable_from_csv("FastBridgeApp\Bridge_Latin_List_Diederich_all_prep_fastbridge_7_2020.csv")

    rareCount = 0
    totalWords = 0
    for word_tuple in text_slice:
        if word_tuple[0] not in hashTable:
            rareCount +=1
        totalWords +=1
    
    lexical_sophistication = rareCount/totalWords
    return lexical_sophistication

def calculate_unique_words(text_object: Text, start_section, end_section):
    '''
    Calculate the total amount of unique words
    '''
    start_index = text_object.sections[start_section]
    end_index = text_object.sections[end_section]
    text_slice = text_object.words[start_index:end_index]

    if start_section == 'start' and end_section == 'end':
        text_slice = text_object.words

    #unique_words = len(set(word[0] for word in text_instance.words))
    unique_words = len(set([word_tuple[0] for word_tuple in text_slice]))
    return unique_words


def get_lexical_variation(text_object: Text, start_section, end_section):   
    num_unique = calculate_unique_words(text_object, start_section, end_section)#V
    total_words = get_number_of_words(text_object, start_section, end_section)#N

    TTR = num_unique/total_words
    RootTTR = num_unique/sqrt(total_words)
    CTTR = num_unique/sqrt(2*total_words)
    LogTTR = log(num_unique)/log(total_words)

    return (TTR, RootTTR, CTTR, LogTTR)


def get_average_subordinations_per_section(start_location_1, start_location_2, end_location_1, end_location_2):
    '''
    Goes into Full AP Excel file for text, so different LOCATION numbers, i.e no more 1.4622, now it should be 1_4
    '''
    df = pd.read_excel("FastBridgeApp\Bridge_Latin_Text_Vergilius_Aeneis_VerAen_newAP_localdef_20230310.xlsx")

    # Split the 'LOCATION' column into two columns: 'LOCATION_1' and 'LOCATION_2'
    df[['LOCATION_1', 'LOCATION_2']] = df['LOCATION'].str.split('_', expand=True).astype(int)

    # Filter the DataFrame
    start_condition = (((df['LOCATION_1'] >= start_location_1) & (df['LOCATION_2'] >= start_location_2)))

    end_condition = (((df['LOCATION_1'] <= end_location_1) & (df['LOCATION_2'] <= end_location_2)))

    df = df[start_condition & end_condition]

    # Count the total number of non-null entries in the 'SUBORDINATION_CODE' column for each section
    subordinations_per_section = df['SUBORDINATION_CODE'].notnull().groupby(df['SECTION']).sum()

    # Count the total number of sections
    num_sections = df['SECTION'].nunique()

    average_subordinations = subordinations_per_section.sum() / num_sections
    return average_subordinations

def calculate_average_word_length(words):
    return sum(len(word) for word in words) / len(words)

def get_avg_word_length(text_object:Text, start_section, end_section):
    '''
    Get mean word length for a section
    '''
    start_index = text_object.sections[start_section]
    end_index = text_object.sections[end_section]
    text_slice = text_object.words[start_index:end_index]

    if start_section == 'start' and end_section == 'end':
        text_slice = text_object.words
    
    sections = []
    for word_tuple in text_slice:
        word = word_tuple[0]
        sections.append(word)

    average_word_length = calculate_average_word_length(sections)
    return average_word_length

def get_gen_lex_r(text_object: Text, start_section, end_section):
    start_index = text_object.sections[start_section]
    end_index = text_object.sections[end_section]
    text_slice = text_object.words[start_index:end_index]

    if start_section == 'start' and end_section == 'end':
        text_slice = text_object.words

    countTokens = 0
    countTitles = 0
    titles = []
    for word_tuple in text_slice:
        countTokens +=1
        word = word_tuple[0]
        if word not in titles:
            countTitles +=1
            titles.append(word)
    
    gen_lex_r = countTokens/sqrt(countTitles)
    return gen_lex_r

def get_gen_lex_c(text_object: Text, start_section, end_section):
    start_index = text_object.sections[start_section]
    end_index = text_object.sections[end_section]
    text_slice = text_object.words[start_index:end_index]

    if start_section == 'start' and end_section == 'end':
        text_slice = text_object.words

    countTokens = 0
    countTitles = 0
    titles = []
    for word_tuple in text_slice:
        countTokens +=1
        word = word_tuple[0]
        if word not in titles:
            countTitles +=1
            titles.append(word)
    
    gen_lex_c = log(countTokens)/log(countTitles)
    return gen_lex_c

def create_word_set(file_path):
    word_set = set()
    with open(file_path, 'r', encoding = 'utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            word_set.add(row['TITLE'])
    return word_set

def get_lex_r(text_object: Text, start_section, end_section):
    #Get the Diederich 300 -> Adjusted CSV method
    diederich300 = set()
    with open("FastBridgeApp\Bridge_Latin_List_Diederich_all_prep_fastbridge_7_2020_BridgeImport.csv", 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        count = 0
        for row in reader:
            if count <=306:#From Latin vocabulary knowledge and the Readability of Latin texts
                diederich300.add(row['TITLE'])
                count +=1
            else:
                break
    
    dcc = create_word_set("FastBridgeApp\Bridge-Vocab-Latin-List-DCC.csv")

    diederich1500 = create_word_set("FastBridgeApp\Bridge_Latin_List_Diederich_all_prep_fastbridge_7_2020_BridgeImport.csv")

    #Stats boilerplate
    start_index = text_object.sections[start_section]
    end_index = text_object.sections[end_section]
    text_slice = text_object.words[start_index:end_index]

    if start_section == 'start' and end_section == 'end':
        text_slice = text_object.words

    #Bad naming standards, these are counting which words are NOT in these lists
    in300 = 0
    inDCC = 0
    in1500 = 0
    countWords = 0
    for word_tuple in text_slice:
        if word_tuple[0] not in diederich300:
            in300 +=1
        if word_tuple[0] not in dcc:
            inDCC +=1
        if word_tuple[0] not in diederich1500:
            in1500 +=1
        countWords +=1

    freq300 = in300/countWords
    freqDCC = inDCC/countWords
    freq1500 = in1500/countWords

    mean_word_length = get_avg_word_length(text_object,start_section,end_section)
    lexical_sophistication = get_lexical_sophistication(text_object, start_section, end_section)
    
    lexical_variation = get_lexical_variation(text_object, start_section, end_section)
    logTTR = lexical_variation[3]
    rootTTR = lexical_variation[1]

    lex_r = ((mean_word_length*0.457)+(freq300*0.063)+(freqDCC*0.076)+(freq1500*0.092)+(lexical_sophistication*0.059)+(logTTR*0.312)+(rootTTR*0.143))
             
    lex_r -=11.7
    lex_r *= 0.833

    return lex_r

#main()

# Using the get_text function to load the text instance
text_instance = get_text('vergil_aeneid_ap_selections', 'Latin').book  

section_start = "start"
section_end = "end"
#4.355
#Call new functions
print(f"Stats for sections: {section_start} - {section_end}")
print(f"Number of words: {get_number_of_words(text_instance, str(section_start), str(section_end))}")
print(f"Vocabulary Size: {get_vocabulary_size(text_instance,str(section_start), str(section_end))}")
#print(f"Hapax Legomena: {get_hapax_legomena(text_instance, str(section_start), str(section_end))}")

#plot_avg_word_length(text_instance, str(section_start), str(section_end))
#plot_avg_word_length2(text_instance, '1.1', '6.899')
plot_word_frequency(text_instance, str(section_start), str(section_end))


#print(f"Lexical Density: {get_lexical_density(text_instance, str(section_start), str(section_end))}")
#The density is way too slow

#print(f"Lexical Sophistication: {get_lexical_sophistication(text_instance,str(section_start), str(section_end))}")
#print(f"Lexical Variation: {get_lexical_variation(text_instance, str(section_start), str(section_end))}")
#print(f"Average Subordinations per Section/Sentence: {get_average_subordinations_per_section(1,1,4,355)}")

print(f"LexR: {get_lex_r(text_instance, str(section_start), str(section_end))}")