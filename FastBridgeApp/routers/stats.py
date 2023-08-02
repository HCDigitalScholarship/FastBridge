import os
import sys
import importlib
from math import log, sqrt
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px
from text import Text
from collections import defaultdict
import spacy  # for LatinCy
import csv  # for hashtable of Diderich -> lexical sophistication
import matplotlib.font_manager as fm
import time
import numpy as np
from scipy.signal import savgol_filter

from fastapi import APIRouter, WebSocket, Request, File, Form, UploadFile, Depends, HTTPException, status
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse

import DefinitionTools
from pathlib import Path
# import matplotlib.ticker as ticker #For the x axis ticks

'''
Files:
Text files -> Text class, get_text().book
Working File -> FastBridgeApp\Bridge_Latin_Text_Vergilius_Aeneis_VerAen_newAP_localdef_20230310.xlsx
Latin Dictionary -> FastBridgeApp\bridge_latin_dictionary.csv
Diederich 300,1500 -> FastBridgeApp\Bridge_Latin_List_Diederich_all_prep_fastbridge_7_2020_BridgeImport.csv
DCC -> FastBridgeApp\Bridge-Vocab-Latin-List-DCC.csv
'''


# Decorators
# times the method you give to it, apply using @timer_decorator above method
def timer_decorator(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        elapsed_time = end_time - start_time
        return result, elapsed_time
    return wrapper


def round_decorator(func):
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)

        if isinstance(result, tuple):
            return tuple(round(val, 2) if isinstance(val, (int, float)) else val for val in result)
        elif isinstance(result, (int, float)):
            return round(result, 2)
        else:
            return result
    return wrapper


# Define FontProperties
prop = fm.FontProperties(family='serif', size=9)

# LatinCy
# pip install https://huggingface.co/latincy/la_core_web_trf/resolve/main/la_core_web_trf-any-py3-none-any.whl

# Seaborn Themes
title_font = {'fontname': 'serif', 'size': '13', 'color': 'black', 'weight': 'normal',
              'verticalalignment': 'bottom'}  # This is for the title properties
axis_font = {'fontname': 'serif', 'size': '11'}  # This is for the axis labels
colorblind_palette = ['#E69F00', '#56B4E9', '#009E73',
                      '#F0E442', '#0072B2', '#D55E00', '#CC79A7']

# Dictionary File


@timer_decorator
def get_latin_dictionary(file_path):  # for reading in DICTIONARY file
    word_dictionary = {}
    with open(file_path, 'r', encoding='utf-8-sig') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            # print(row)  # Add this line
            if 'TITLE' in row:
                word_dictionary[row['TITLE']] = row
            else:
                print(row)
            # Use the 'TITLE' field as the key, and store the entire row (which is a dictionary) as the value
            # word_dictionary[row["TITLE"]] = row
    return word_dictionary


latin_dict, elapsed_time = get_latin_dictionary(
    "/home/microbeta/crim/FastBridge/FastBridgeApp/bridge_latin_dictionary.csv")
print("Loaded Latin Dictionary: {} seconds".format(elapsed_time))

# Get Diederich


@timer_decorator
def create_hashtable_from_csv(file_path):
    hashtable = {}
    with open(file_path, 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            hashtable[row['TITLE']] = {'LOCATION': row['LOCATION'], 'SECTION': row['SECTION'],
                                       'RUNNINGCOUNT': row['RUNNINGCOUNT'], 'TEXT': row['TEXT']}
    return hashtable


print(os.getcwd())
diederich, diederich_time = create_hashtable_from_csv(
    "/home/microbeta/crim/FastBridge/FastBridgeApp/Bridge_Latin_List_Diederich_all_prep_fastbridge_7_2020_BridgeImport.csv")
print("Loaded Diederich HashTable: {} seconds".format(diederich_time))

# Get DCC


@timer_decorator
# For getting the unique tokens, or vocabulary, NO DUPLICATES
def create_word_set(file_path):
    word_set = set()
    with open(file_path, 'r', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            word_set.add(row['TITLE'])
    return word_set


@timer_decorator
def get_diederich300(file_path):
    diederich300 = set()
    with open(file_path, 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        count = 0
        for row in reader:
            if count <= 306:  # From Latin vocabulary knowledge and the Readability of Latin texts
                diederich300.add(row['TITLE'])
                count += 1
            else:
                break
    return diederich300
# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$


def get_text(form_request: str, language: str):
    """
    Imports the text that was requested. This way, we only load the texts that the user is requesting each time.
    """
    return importlib.import_module(f'data.{language}.{form_request}')  # point to the data folder


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


###############
def get_slice(text_object: Text, start_section, end_section):
    start_index = text_object.sections[start_section]
    end_index = text_object.sections[end_section]
    text_slice = text_object.words[start_index:end_index]

    if start_section == 'start' and end_section == 'end':
        text_slice = text_object.words

    return text_slice


def find_hapax_legomena(words):
    word_frequencies = defaultdict(int)
    for word in words:
        word_frequencies[word] += 1
    return [word for word, freq in word_frequencies.items() if freq == 1]

# Class that the site uses to handle everything


class TextAnalyzer():

    def __init__(self, dictionary_path: str, diederich_path: str, dcc_path: str):

        self.dictionary, self.dictionary_time = get_latin_dictionary(
            dictionary_path)
        print("Dictionary Loaded: {} seconds".format(self.dictionary_time))

        self.diederich, self.diederich_time = create_hashtable_from_csv(
            diederich_path)
        print("Diederich 1500 Loaded: {} seconds".format(self.diederich_time))

        self.diederich300, self.diederich300_time = get_diederich300(
            diederich_path)
        print("Diederich 300 Loaded: {} seconds".format(self.diederich300_time))

        self.dcc, self.dcc_time = create_word_set(dcc_path)
        print("DCC Loaded: {} seconds".format(self.dcc_time))

        self.texts = []  # (Text, start section, end section)

    # Add working file for subordinations/section?
    def add_text(self, form_request: str, language: str, start_section, end_section):
        self.texts.append(
            (get_text(form_request, language).book, start_section, end_section))

    def get_textname(self):
        if len(self.texts) == 0:
            return -1
        elif len(self.texts) == 1:
            return self.texts[0][0].name
        else:
            print()

    def num_words(self) -> int:
        if len(self.texts) == 0:
            return -1
        elif len(self.texts) == 1:
            start_index = self.texts[0][0].sections[self.texts[0][1]]
            end_index = self.texts[0][0].sections[self.texts[0][2]]
            word_count = end_index - start_index
            if self.texts[0][1] == 'start' and self.texts[0][2] == 'end':
                word_count = self.texts[0][0].words[-1][1]
            return word_count
        else:
            sum = 0
            for text in self.texts:
                start_index = text[0].sections[text[1]]
                end_index = text[0].sections[text[2]]
                word_count = end_index - start_index
                if text[1] == 'start' and text[2] == 'end':
                    word_count = text[0].words[-1][1]
                sum += word_count
            return word_count

    def vocab_size(self) -> int:
        if len(self.texts) == 0:
            return -1
        elif len(self.texts) == 1:
            text_slice = get_slice(
                self.texts[0][0], self.texts[0][1], self.texts[0][2])
            vocabulary = set(word[0] for word in text_slice)
            return len(vocabulary)
        else:
            vocab = set()
            for text in self.texts:
                text_slice = get_slice(text[0], text[1], text[2])
                vocabulary = set(word[0] for word in text_slice)
                vocab = vocab.union(vocabulary)
            return len(vocab)

    @round_decorator
    def hapax_legonema(self, tupleFlag = False):
        if len(self.texts) == 0:
            return []
        elif len(self.texts) == 1:
            text_slice = get_slice(
                self.texts[0][0], self.texts[0][1], self.texts[0][2])
            allwords = []
            for word_tuple in text_slice:
                word = word_tuple[2]
                allwords.append(word)
            hapax_legomena = find_hapax_legomena(allwords)
            hapax_legomena = sorted(hapax_legomena)  # Sort the hapax legomena
            percentage = len(hapax_legomena) / len(allwords) * \
                100  # Calculate the percentage
            if tupleFlag == True:
                return (hapax_legomena, percentage)
            else:
                return hapax_legomena, percentage
            
            return hapax_legomena
        else:
            allwords = []
            for text in self.texts:
                text_slice = get_slice(text[0], text[1], text[2])
                for word_tuple in text_slice:
                    word = word_tuple[0]
                    allwords.append(word)
            hapax_legomena = find_hapax_legomena(allwords)
            return hapax_legomena

    @round_decorator
    def lex_density(self):
        lexicalCategories = ["Adjective", "Adverb", "Noun", "Verb"]
        if len(self.texts) == 0:
            return -1
        elif len(self.texts) == 1:
            text_slice = get_slice(
                self.texts[0][0], self.texts[0][1], self.texts[0][2])
            lexicalSum = 0
            for word_tuple in text_slice:
                word = word_tuple[0]
                if word in self.dictionary:
                    if self.dictionary[word]["PART_OF_SPEECH"] in lexicalCategories:
                        lexicalSum += 1

            total_words = self.num_words()
            lexical_density = lexicalSum/total_words
            return lexical_density
        else:
            lexicalSum = 0
            for text in self.texts:
                text_slice = get_slice(text[0], text[1], text[2])
                for word_tuple in text_slice:
                    word = word_tuple[0]
                    if word in self.dictionary:
                        if self.dictionary[word]["PART_OF_SPEECH"] in lexicalCategories:
                            lexicalSum += 1
            total_words = self.num_words()  # MAKE SURE THIS IS WORKING WITH MULTIPLE TEXTS
            lexical_density = lexicalSum/total_words
            return lexical_density

    @round_decorator
    def lex_sophistication(self):
        if len(self.texts) == 0:
            return -1
        elif len(self.texts) == 1:
            text_slice = get_slice(
                self.texts[0][0], self.texts[0][1], self.texts[0][2])

            rareCount = 0
            totalWords = 0
            for word_tuple in text_slice:
                if word_tuple[0] not in self.diederich:
                    rareCount += 1
                totalWords += 1

            lexical_sophistication = rareCount/totalWords
            return lexical_sophistication
        else:
            rareCount = 0
            totalWords = 0
            for text in self.texts:
                text_slice = get_slice(text[0], text[1], text[2])
                for word_tuple in text_slice:
                    if word_tuple[0] not in self.diederich:
                        rareCount += 1
                totalWords += 1
            lexical_sophistication = rareCount/totalWords
            return lexical_sophistication

    @round_decorator
    def lex_variation(self):
        if len(self.texts) == 0:
            return -1
        elif len(self.texts) == 1:
            text_slice = get_slice(
                self.texts[0][0], self.texts[0][1], self.texts[0][2])
            num_unique = len(set([word_tuple[0]
                             for word_tuple in text_slice]))  # V
            total_words = self.num_words()  # N

            TTR = num_unique/total_words
            RootTTR = num_unique/sqrt(total_words)
            CTTR = num_unique/sqrt(2*total_words)
            LogTTR = log(num_unique)/log(total_words)

            return (TTR, RootTTR, CTTR, LogTTR)
        else:
            total_unique = 0
            for text in self.texts:
                text_slice = get_slice(text[0], text[1], text[2])
                # V for current text selection
                num_unique = len(set([word_tuple[0]
                                 for word_tuple in text_slice]))
                total_unique += num_unique
            total_words = self.num_words()  # N

            TTR = total_unique/total_words
            RootTTR = total_unique/sqrt(total_words)
            CTTR = total_unique/sqrt(2*total_words)
            LogTTR = log(total_unique)/log(total_words)

            return (TTR, RootTTR, CTTR, LogTTR)

    @round_decorator
    def LexR(self):
        properNounCats = ["1", "T"]
        if len(self.texts) == 0:
            return -1
        elif len(self.texts) == 1:
            text_slice = get_slice(
                self.texts[0][0], self.texts[0][1], self.texts[0][2])
            out300 = 0
            outDCC = 0
            out1500 = 0
            countWords = 0
            words = []
            for word_tuple in text_slice:
                if word_tuple[0] in self.dictionary:
                    if self.dictionary[word_tuple[0]]["PROPER"] not in properNounCats:
                        if word_tuple[0] not in self.diederich300:
                            out300 += 1
                        if word_tuple[0] not in self.dcc:
                            outDCC += 1
                        if word_tuple[0] not in self.diederich:
                            out1500 += 1
                        countWords += 1
                        words.append(word_tuple[0])
            freq300 = (out300/countWords)*100
            freqDCC = (outDCC/countWords)*100
            freq1500 = (out1500/countWords)*100

            mean_word_length = sum(len(word) for word in words) / len(words)
            print(f"Mean word length: {mean_word_length}")
            print(f"freq300: {freq300}")
            print(f"freqDCC: {freqDCC}")
            print(f"freq1500: {freq1500}")

            lex_r = ((mean_word_length*0.457)+(freq300*0.063)+(freqDCC*0.076)+(freq1500*0.092) +
                     (self.lex_sophistication()*0.059) + (self.lex_variation()[3]*0.312)+(self.lex_variation()[1]*0.143))

            lex_r -= 11.7
            lex_r += 6
            lex_r *= 0.833

            return lex_r
        else:
            out300 = 0
            outDCC = 0
            out1500 = 0
            countWords = 0
            words = []
            for text in self.texts:
                text_slice = get_slice(text[0], text[1], text[2])
                for word_tuple in text_slice:
                    if word_tuple[0] in self.dictionary:
                        if self.dictionary[word_tuple[0]]["PROPER"] not in properNounCats:
                            if word_tuple[0] not in self.diederich300:
                                out300 += 1
                            if word_tuple[0] not in self.dcc:
                                outDCC += 1
                            if word_tuple[0] not in self.diederich:
                                out1500 += 1
                            countWords += 1
                            words.append(word_tuple[0])

            freq300 = (out300/countWords)*100
            freqDCC = (outDCC/countWords)*100
            freq1500 = (out1500/countWords)*100

            mean_word_length = sum(len(word) for word in words) / len(words)
            lex_r = ((mean_word_length*0.457)+(freq300*0.063)+(freqDCC*0.076)+(freq1500*0.092) +
                     (self.lex_sophistication()*0.059)+(self.lex_variation()[3]*0.312)+(self.lex_variation()[1]*0.143))

            lex_r -= 11.7
            lex_r += 6
            lex_r *= 0.833
            return lex_r

    def totalWordsNoProper(self):
        if len(self.texts) == 0:
            return -1
        elif len(self.texts) == 1:
            text_slice = get_slice(
                self.texts[0][0], self.texts[0][1], self.texts[0][2])
            # Go through the words of text_slice
            # Connect to Dictionary to filter out PROPER, "1" and "T"
            words = []
            for word_tuple in text_slice:
                word = word_tuple[0]
                # filter out proper nouns
                if word in latin_dict and latin_dict[word]["PROPER"] not in ["1", "T"]:
                    words.append(word)

            return len(words)
        else:
            print()

    def uniqueWordsNoProper(self):
        if len(self.texts) == 0:
            return -1
        elif len(self.texts) == 1:
            text_slice = get_slice(
                self.texts[0][0], self.texts[0][1], self.texts[0][2])
            # Go through the words of text_slice
            # Connect to Dictionary to filter out PROPER, "1" and "T"
            words = []
            for word_tuple in text_slice:
                word = word_tuple[0]
                # filter out proper nouns
                if word in latin_dict and latin_dict[word]["PROPER"] not in ["1", "T"]:
                    words.append(word)

                vocabulary = set(word for word in words)
            return len(vocabulary)
        else:
            print()

    def top20NoDie300(self):
        if len(self.texts) == 0:
            return -1
        elif len(self.texts) == 1:
            text_slice = get_slice(
                self.texts[0][0], self.texts[0][1], self.texts[0][2])
            # Go through the words of text_slice
            # Connect to Dictionary to filter out PROPER, "1" and "T"
            words = []

            for word_tuple in text_slice:
                if word_tuple[0] in latin_dict:
                    if int(latin_dict[word_tuple[0]]["CORPUSFREQ"]) <= 300:
                        continue
                    words.append(word_tuple[2])
                else:
                    words.append(word_tuple[2])

            word_counts = {}


            for word in words:
                if word in word_counts:
                    word_counts[word] += 1
                else:
                    word_counts[word] = 1

            # Sort the dictionary by value in descending order and get the top 20
            top_20_words = sorted(word_counts.items(), key=lambda x: x[1], reverse=True)[:20]
            
            # Extract words from the tuples
            top_20_words = [word for word, freq in top_20_words]
            
            return top_20_words


              # word = word_tuple[0]
              # words.append(word)
              # filter out proper nouns
              # if word in latin_dict and latin_dict[word]["PROPER"] not in ["1", "T"]:
                   # words.append(word)

    @round_decorator
    def freqBinMetrics(self):
        if len(self.texts) == 0:
            return -1
        elif len(self.texts) == 1:
            text_slice = get_slice(
                self.texts[0][0], self.texts[0][1], self.texts[0][2])
            # Go through the words of text_slice
            # Connect to Dictionary to filter out PROPER, "1" and "T"
            words = []
            for word_tuple in text_slice:
                word = word_tuple[0]
                # filter out proper nouns
                if word in latin_dict and latin_dict[word]["PROPER"] not in ["1", "T"]:
                    words.append(word)

            count0_200 = 0
            count201_500 = 0
            count501_1000 = 0
            count1001_1500 = 0
            count1501_2500 = 0
            count2500plus = 0

            for word in words:
                if word in latin_dict:
                    if int(latin_dict[word]["CORPUSFREQ"]) <= 200:
                        count0_200 += 1
                        continue
                    if int(latin_dict[word]["CORPUSFREQ"]) > 200 and int(latin_dict[word]["CORPUSFREQ"]) <= 500:
                        count201_500 += 1
                        continue
                    if int(latin_dict[word]["CORPUSFREQ"]) > 500 and int(latin_dict[word]["CORPUSFREQ"]) <= 1000:
                        count501_1000 += 1
                        continue
                    if int(latin_dict[word]["CORPUSFREQ"]) > 1000 and int(latin_dict[word]["CORPUSFREQ"]) <= 1500:
                        count1001_1500 += 1
                        continue
                    if int(latin_dict[word]["CORPUSFREQ"]) > 1500 and int(latin_dict[word]["CORPUSFREQ"]) <= 2500:
                        count1501_2500 += 1
                        continue
                    if int(latin_dict[word]["CORPUSFREQ"]) > 2500:
                        count2500plus += 1
                        continue

            freq_0_200 = (count0_200/len(words))*100
            freq_201_500 = (count201_500/len(words))*100
            freq_501_1000 = (count501_1000/len(words))*100
            freq_1001_1500 = (count1001_1500/len(words))*100
            freq_1501_2500 = (count1501_2500/len(words))*100
            freq_2500_plus = (count2500plus/len(words))*100

            

            return (freq_0_200, freq_201_500, freq_501_1000, freq_1001_1500,freq_1501_2500,freq_2500_plus)

        else:
            print()
             

    @round_decorator
    def avgWordLength(self):
        if len(self.texts) == 0:
            return -1
        elif len(self.texts) == 1:
            text_slice = get_slice(
                self.texts[0][0], self.texts[0][1], self.texts[0][2])
            # Go through the words of text_slice
            # Connect to Dictionary to filter out PROPER, "1" and "T"
            words = []
            for word_tuple in text_slice:
                words.append(word_tuple[0])

            return sum(len(word) for word in words) / len(words)
        else:
            print()

    def plot_word_freq(self, plot_num = 1):
        if len(self.texts) == 0:
            return
        elif len(self.texts) == 1:
            text_slice = get_slice(
                self.texts[0][0], self.texts[0][1], self.texts[0][2])
            df = pd.DataFrame(text_slice, columns=[
                              "Word", "Index", "Lemma", "Definition", "Notes", "Section", "Word Count"])
            word_frequency = df['Word'].value_counts().reset_index()
            word_frequency.columns = ['Word', 'Frequency']

            sns.set_style("ticks")
            sns.set_context("paper")
            plt.figure(figsize=(10, 5))
            sns.barplot(
                data=word_frequency[:30], x='Word', y='Frequency', palette=colorblind_palette)
            sns.despine()
            plt.title(
                f"Word Frequency of {self.texts[0][0].name}", **title_font)
            plt.xlabel('Word', **axis_font)
            plt.ylabel('Frequency', **axis_font)
            plt.xticks(rotation=90)

            # Get the current Axes instance
            ax = plt.gca()

            # set font properties to x and y tick labels
            plt.setp(ax.get_xticklabels(), fontproperties=prop)
            plt.setp(ax.get_yticklabels(), fontproperties=prop)

            # Save plot as an image file instead of showing
            # replace with the actual path and name
            plot_path = f'/home/microbeta/crim/FastBridge/FastBridgeApp/static/assets/plots/plot{plot_num}.png'
            plt.savefig(plot_path)
            plt.close()  # close the plot

            return plot_path  # return the file path of the saved plot
        else:
            text_slices_concat = []
            for text in self.texts:
                text_slices_concat += get_slice(text[0], text[1], text[2])

            df = pd.DataFrame(text_slices_concat, columns=[
                              "Word", "Index", "Lemma", "Definition", "Notes", "Section", "Word Count"])
            word_frequency = df['Word'].value_counts().reset_index()
            word_frequency.columns = ['Word', 'Frequency']

            sns.set_style("ticks")
            sns.set_context("paper")
            plt.figure(figsize=(10, 5))
            sns.barplot(
                data=word_frequency[:30], x='Word', y='Frequency', palette=colorblind_palette)
            sns.despine()
            # CHANGE this to include all names
            plt.title(
                f"Word Frequency of {self.texts[0][0].name}", **title_font)
            plt.xlabel('Word', **axis_font)
            plt.ylabel('Frequency', **axis_font)
            plt.xticks(rotation=90)

            # Get the current Axes instance
            ax = plt.gca()

            # set font properties to x and y tick labels
            plt.setp(ax.get_xticklabels(), fontproperties=prop)
            plt.setp(ax.get_yticklabels(), fontproperties=prop)

            # Save plot as an image file instead of showing
            # replace with the actual path and name
            plot_path = f'/home/microbeta/crim/FastBridge/FastBridgeApp/static/assets/plots/plot{plot_num}.png'
            plt.savefig(plot_path)
            plt.close()  # close the plot

            return plot_path  # return the file path of the saved plot

    def plot_lin_lex_load(self, rolling_window_size=25, plot_num = 3):
        if len(self.texts) == 0:
            return -1
        elif len(self.texts) == 1:
            text_slice = get_slice(
                self.texts[0][0], self.texts[0][1], self.texts[0][2])
            words = []
            scores = []
            for word_tuple in text_slice:
                word = word_tuple[0]
                # filter out proper nouns
                if word in latin_dict and latin_dict[word]["PROPER"] not in ["1", "T"]:
                    words.append(word)

            for word in words:
                if word in latin_dict:
                    if int(latin_dict[word]["CORPUSFREQ"]) <= 200:
                        scores.append(2)
                        continue
                    if int(latin_dict[word]["CORPUSFREQ"]) > 200 and int(latin_dict[word]["CORPUSFREQ"]) <= 1000:
                        scores.append(1)
                        continue
                    if int(latin_dict[word]["CORPUSFREQ"]) > 1000 and int(latin_dict[word]["CORPUSFREQ"]) <= 2000:
                        scores.append(-1)
                        continue
                    if int(latin_dict[word]["CORPUSFREQ"]) > 2000 and int(latin_dict[word]["CORPUSFREQ"]) <= 5000:
                        scores.append(-2)
                        continue
                    if int(latin_dict[word]["CORPUSFREQ"]) > 5000:
                        scores.append(-4)
                        continue
                else:
                    scores.append(-4)
                    continue

            # Calculate rolling average of the scores
            rolling_average = pd.Series(scores).rolling(
                window=rolling_window_size).mean()

            # Apply Savitzky-Golay filter
            # window size 51, polynomial order 3
            smoothed_scores = savgol_filter(rolling_average, 101, 3)

            x_indexes = list(range(len(words)))

            # calculate average linear lexical score for the entire text
            average_score = np.mean(scores)

            sns.set_style("ticks")
            sns.set_context("paper")
            plt.figure(figsize=(10, 5))


            #attempt at overlaying sections onto x axis, seems to be too many sections to render properly
            # section_words = self.texts[0][0].sections

            # # create a list of tick locations and labels
            # tick_locations = list(section_words.values())
            # tick_locations.pop(-1)
            # tick_locations.pop(-2)

            # tick_labels = list(section_words.keys())
            # tick_labels.remove('start')
            # tick_labels.remove('end')
            
            sns.lineplot(x=x_indexes, y=smoothed_scores,
                         errorbar=None, color=colorblind_palette[6])

            # add a horizontal line representing the average linear lexical score
            plt.axhline(y=average_score,
                        color=colorblind_palette[4], linestyle='--')
            
         
            sns.despine()
            plt.title(
                f"Linear Lexical Load of {self.texts[0][0].name}", **title_font)
            plt.xlabel('Word', **axis_font)
            plt.ylabel(
                f'{rolling_window_size}-Word Rolling Average of Linear Lexical Load Score', **axis_font)

            # Get the current Axes instance
            ax = plt.gca()

            # set x-axis ticks to window size?  -> Only activate this if you want to see all the numbers jumble up at the bottom
            # tick_spacing = rolling_window_size  # change this to the size of your slices
            # ax.xaxis.set_major_locator(ticker.MultipleLocator(tick_spacing))

            # set font properties to x and y tick labels
            plt.setp(ax.get_xticklabels(), fontproperties=prop)
            plt.setp(ax.get_yticklabels(), fontproperties=prop)




            # Save plot as an image file instead of showing
            # replace with the actual path and name
            plot_path = f'/home/microbeta/crim/FastBridge/FastBridgeApp/static/assets/plots/plot{plot_num}.png'
            plt.savefig(plot_path)
            plt.close()  # close the plot

            return plot_path  # return the file path of the saved plot
        else:
            # WHEN WE FIGURE OUT WHAT TO DO WITH MULTIPLE TEXT SELECTIONS, CODE HERE, WILL HAVE TO ADD HTML STRUCTURE DYNAMICALLY TO CONTAIN MANY PLOTS
            print()

    def plot_cum_lex_load(self, plot_num = 2):
        if len(self.texts) == 0:
            return -1
        elif len(self.texts) == 1:
            text_slice = get_slice(
                self.texts[0][0], self.texts[0][1], self.texts[0][2])
            # Go through the words of text_slice
            # Connect to Dictionary to filter out PROPER, "1" and "T"
            words = []
            scores = []
            for word_tuple in text_slice:
                word = word_tuple[0]
                # filter out proper nouns
                if word in latin_dict and latin_dict[word]["PROPER"] not in ["1", "T"]:
                    words.append(word)

            for word in words:
                if word in latin_dict:
                    if int(latin_dict[word]["CORPUSFREQ"]) <= 200:
                        scores.append(2)
                        continue
                    if int(latin_dict[word]["CORPUSFREQ"]) > 200 and int(latin_dict[word]["CORPUSFREQ"]) <= 1000:
                        scores.append(1)
                        continue
                    if int(latin_dict[word]["CORPUSFREQ"]) > 1000 and int(latin_dict[word]["CORPUSFREQ"]) <= 2000:
                        scores.append(-1)
                        continue
                    if int(latin_dict[word]["CORPUSFREQ"]) > 2000 and int(latin_dict[word]["CORPUSFREQ"]) <= 5000:
                        scores.append(-2)
                        continue
                    if int(latin_dict[word]["CORPUSFREQ"]) > 5000:
                        scores.append(-4)
                        continue
                else:
                    scores.append(-4)
                    continue

            cumulative_scores = np.cumsum(scores)

            # Calculate rolling average
            # rolling_average = pd.Series(cumulative_scores).rolling(window=rolling_window_size).mean()

            x_indexes = list(range(len(words)))

            sns.set_style("ticks")
            sns.set_context("paper")
            plt.figure(figsize=(10, 5))
            sns.lineplot(x=x_indexes, y=cumulative_scores,
                         errorbar=None, color=colorblind_palette[2])
            sns.despine()
            plt.title(
                f"Cumulative Lexical Load of {self.texts[0][0].name}", **title_font)
            plt.xlabel('Word', **axis_font)
            plt.ylabel('Cumulative Lexical Load Score', **axis_font)

            # Get the current Axes instance
            ax = plt.gca()

            # set font properties to x and y tick labels
            plt.setp(ax.get_xticklabels(), fontproperties=prop)
            plt.setp(ax.get_yticklabels(), fontproperties=prop)

            # Save plot as an image file instead of showing
            # replace with the actual path and name
            plot_path = f'/home/microbeta/crim/FastBridge/FastBridgeApp/static/assets/plots/plot{plot_num}.png'
            plt.savefig(plot_path)
            plt.close()  # close the plot

            return plot_path
        else:
            print()

    def plot_freq_bin(self, plot_num = 4):
        if len(self.texts) == 0:
            return -1
        elif len(self.texts) == 1:
            text_slice = get_slice(
                self.texts[0][0], self.texts[0][1], self.texts[0][2])
            # Go through the words of text_slice
            # Connect to Dictionary to filter out PROPER, "1" and "T"
            words = []
            for word_tuple in text_slice:
                word = word_tuple[0]
                # filter out proper nouns
                if word in latin_dict and latin_dict[word]["PROPER"] not in ["1", "T"]:
                    words.append(word)

            count0_200 = 0
            count201_500 = 0
            count501_1000 = 0
            count1001_1500 = 0
            count1501_2500 = 0
            count2500plus = 0

            for word in words:
                if word in latin_dict:
                    if int(latin_dict[word]["CORPUSFREQ"]) <= 200:
                        count0_200 += 1
                        continue
                    if int(latin_dict[word]["CORPUSFREQ"]) > 200 and int(latin_dict[word]["CORPUSFREQ"]) <= 500:
                        count201_500 += 1
                        continue
                    if int(latin_dict[word]["CORPUSFREQ"]) > 500 and int(latin_dict[word]["CORPUSFREQ"]) <= 1000:
                        count501_1000 += 1
                        continue
                    if int(latin_dict[word]["CORPUSFREQ"]) > 1000 and int(latin_dict[word]["CORPUSFREQ"]) <= 1500:
                        count1001_1500 += 1
                        continue
                    if int(latin_dict[word]["CORPUSFREQ"]) > 1500 and int(latin_dict[word]["CORPUSFREQ"]) <= 2500:
                        count1501_2500 += 1
                        continue
                    if int(latin_dict[word]["CORPUSFREQ"]) > 2500:
                        count2500plus += 1
                        continue

            freq_0_200 = count0_200/len(words)
            freq_201_500 = count201_500/len(words)
            freq_501_1000 = count501_1000/len(words)
            freq_1001_1500 = count1001_1500/len(words)
            freq_1501_2500 = count1501_2500/len(words)
            freq_2500_plus = count2500plus/len(words)

            data = {'Frequency Range': ['0-200', '201-500', '501-1000', '1001-1500', '1501-2500', '2500+'],
                    'Percentage of Words': [freq_0_200, freq_201_500, freq_501_1000, freq_1001_1500, freq_1501_2500, freq_2500_plus]}

            df = pd.DataFrame(data)

            sns.set_style("ticks")
            sns.set_context("paper")
            plt.figure(figsize=(10, 5))
            barplot = sns.barplot(
                x='Frequency Range', y='Percentage of Words', data=df, palette=colorblind_palette)
            sns.despine()
            plt.title('Percentage of Words in Frequency Ranges', **
                      title_font)            # Get the current Axes instance
            ax = plt.gca()

            # set font properties to x and y tick labels
            plt.setp(ax.get_xticklabels(), fontproperties=prop)
            plt.setp(ax.get_yticklabels(), fontproperties=prop)

            plt.xlabel('Frequency Range', **axis_font)
            plt.ylabel('Percentage of Words', **axis_font)

            # add the values on the bars
            for p in barplot.patches:
                barplot.annotate(format(p.get_height(), '.2f'),
                                 (p.get_x() + p.get_width() / 2., p.get_height()),
                    ha= 'center', va = 'center',
                    xytext= (0, 10),
                    textcoords='offset points')

            # Save plot as an image file instead of showing
            # replace with the actual path and name
            plot_path = f'/home/microbeta/crim/FastBridge/FastBridgeApp/static/assets/plots/plot{plot_num}.png'
            plt.savefig(plot_path)
            plt.close()  # close the plot

            return plot_path

        else:
            print()

    def __str__(self) -> str:
        toReturn = ""
        toReturn += f"Number of words:\t{self.num_words()}\n"
        toReturn += f"Vocabulary Size:\t{self.vocab_size()}\n"
        toReturn += f"Hapax Legonema:\t{self.hapax_legonema()}\n"
        toReturn += f"Lexical Density:\t{self.lex_density()}\n"
        toReturn += f"Lexical Sophistication:\t{self.lex_sophistication()}\n"
        toReturn += f"Lexical Variation:\t{self.lex_variation()}\n"
        toReturn += f"LexR:\t{self.LexR()}\n"
        return toReturn


##########################################################################################

# All functions below the hashtag line can find attributes of text in specific sections

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

    df = pd.DataFrame(text_slice, columns=[
                      "Word", "Index", "Lemma", "Definition", "Notes", "Section", "Word Count"])
    df['Word Length'] = df['Word'].apply(len)
    avg_word_length = df.groupby('Section')['Word Length'].mean().reset_index()

    # determine the step size for x-axis labels
    n_sections = avg_word_length['Section'].nunique()
    # adjust this factor to change the number of labels displayed
    step_size = max(1, n_sections // 20)

    plt.figure(figsize=(10, 5))

    sns.set_style("ticks")
    sns.set_context("paper")
    lineplot = sns.barplot(data=avg_word_length, x='Section',
                           y='Word Length', palette=colorblind_palette, width=0.9)
    sns.despine()
    plt.title(
        f"Average Word Length per Section of {text_object.name}", **title_font)
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

    df = pd.DataFrame(text_slice, columns=[
                      "Word", "Index", "Lemma", "Definition", "Notes", "Section", "Word Count"])
    df['Word Length'] = df['Word'].apply(len)
    avg_word_length = df.groupby('Section')['Word Length'].mean().reset_index()

    # determine the step size for x-axis labels
    n_sections = avg_word_length['Section'].nunique()
    # adjust this factor to change the number of labels displayed
    step_size = max(1, n_sections // 20)

    fig = px.bar(avg_word_length, x='Section', y='Word Length',
                 hover_data=['Word Length'], labels={'Word Length': 'Average Word Length per Section'})

    fig.update_layout(
        autosize=False,
        width=1000,
        height=500,
        xaxis_tickangle=-90,
    )

    fig.update_xaxes(
        tickmode='array',
        tickvals=avg_word_length['Section'][::step_size]
    )

    fig.show()


# Function to display distribution of word frequency
def plot_word_frequency(text_object: Text, start_section, end_section):
    start_index = text_object.sections[start_section]
    end_index = text_object.sections[end_section]
    text_slice = text_object.words[start_index:end_index]

    if start_section == 'start' and end_section == 'end':
        text_slice = text_object.words

    df = pd.DataFrame(text_slice, columns=[
                      "Word", "Index", "Lemma", "Definition", "Notes", "Section", "Word Count"])
    word_frequency = df['Word'].value_counts().reset_index()
    word_frequency.columns = ['Word', 'Frequency']

    sns.set_style("ticks")
    sns.set_context("paper")
    plt.figure(figsize=(10, 5))
    sns.barplot(data=word_frequency[:30], x='Word',
                y='Frequency', palette=colorblind_palette)
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


def get_hapax_legomena(text_object: Text, start_section, end_section):
    '''
    Returns all of the words used once from each section, separated by section, it's just printing but can return in zip()
    '''
    # Get words from each section
    # sections = defaultdict(list)
    allwords = []
    start_index = text_object.sections[start_section]
    end_index = text_object.sections[end_section]
    text_slice = text_object.words[start_index:end_index]

    if start_section == 'start' and end_section == 'end':
        text_slice = text_object.words

    for word_tuple in text_slice:
        word = word_tuple[0]
        section = word_tuple[5]
        # sections[section].append(word)
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
    # nlp = spacy.load("la_core_web_trf")
    start_index = text_object.sections[start_section]
    end_index = text_object.sections[end_section]
    text_slice = text_object.words[start_index:end_index]

    if start_section == 'start' and end_section == 'end':
        text_slice = text_object.words

    # FINDING LEXICAL WORDS
    # spacyString = ""

    lexicalCategories = ["Adjective", "Adverb", "Noun", "Verb"]
    lexicalSum = 0
    for word_tuple in text_slice:
        word = word_tuple[0]
        if word in latin_dict:
            if latin_dict[word]["PART_OF_SPEECH"] in lexicalCategories:
                lexicalSum += 1

        # if len(spacyString) == 0:
        #     spacyString = word
        # else:
        #     spacyString += f" {word}"

    # doc = nlp(spacyString)

    # lexicalSum = 0
    # lexicalCategories = ['NOUN', 'ADV', 'PROPN', 'ADJ', 'VERB']
    # for token in doc:
    #     if token.pos_ in lexicalCategories:
    #         lexicalSum += 1

    # FINDING TOTAL WORDS IN SECTION
    total_words = get_number_of_words(text_object, start_section, end_section)

    lexical_density = lexicalSum/total_words

    return lexical_density


def get_lexical_sophistication(text_object: Text, start_section, end_section):
    # import os
    # print(os.getcwd())

    start_index = text_object.sections[start_section]
    end_index = text_object.sections[end_section]
    text_slice = text_object.words[start_index:end_index]

    if start_section == 'start' and end_section == 'end':
        text_slice = text_object.words

    hashTable = create_hashtable_from_csv(
        "/home/microbeta/crim/FastBridge/FastBridgeApp/Bridge_Latin_List_Diederich_all_prep_fastbridge_7_2020.csv")

    rareCount = 0
    totalWords = 0
    for word_tuple in text_slice:
        if word_tuple[0] not in hashTable:
            rareCount += 1
        totalWords += 1

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

    # unique_words = len(set(word[0] for word in text_instance.words))
    unique_words = len(set([word_tuple[0] for word_tuple in text_slice]))
    return unique_words


def get_lexical_variation(text_object: Text, start_section, end_section):
    num_unique = calculate_unique_words(
        text_object, start_section, end_section)  # V
    total_words = get_number_of_words(
        text_object, start_section, end_section)  # N

    TTR = num_unique/total_words
    RootTTR = num_unique/sqrt(total_words)
    CTTR = num_unique/sqrt(2*total_words)
    LogTTR = log(num_unique)/log(total_words)

    return (TTR, RootTTR, CTTR, LogTTR)


def get_average_subordinations_per_section(start_location_1, start_location_2, end_location_1, end_location_2):
    '''
    Goes into Full AP Excel file for text, so different LOCATION numbers, i.e no more 1.4622, now it should be 1_4
    '''
    df = pd.read_excel(
        "FastBridgeApp\Bridge_Latin_Text_Vergilius_Aeneis_VerAen_newAP_localdef_20230310.xlsx")

    # Split the 'LOCATION' column into two columns: 'LOCATION_1' and 'LOCATION_2'
    df[['LOCATION_1', 'LOCATION_2']] = df['LOCATION'].str.split(
        '_', expand=True).astype(int)

    # Filter the DataFrame
    start_condition = (((df['LOCATION_1'] >= start_location_1) & (
        df['LOCATION_2'] >= start_location_2)))

    end_condition = (((df['LOCATION_1'] <= end_location_1)
                     & (df['LOCATION_2'] <= end_location_2)))

    df = df[start_condition & end_condition]

    # Count the total number of non-null entries in the 'SUBORDINATION_CODE' column for each section
    subordinations_per_section = df['SUBORDINATION_CODE'].notnull().groupby(
        df['SECTION']).sum()

    # Count the total number of sections
    num_sections = df['SECTION'].nunique()

    average_subordinations = subordinations_per_section.sum() / num_sections
    return average_subordinations


def calculate_average_word_length(words):
    return sum(len(word) for word in words) / len(words)


def get_avg_word_length(text_object: Text, start_section, end_section):
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
        countTokens += 1
        word = word_tuple[0]
        if word not in titles:
            countTitles += 1
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
        countTokens += 1
        word = word_tuple[0]
        if word not in titles:
            countTitles += 1
            titles.append(word)

    gen_lex_c = log(countTokens)/log(countTitles)
    return gen_lex_c


def get_lex_r(text_object: Text, start_section, end_section):
    # Get the Diederich 300 -> Adjusted CSV method
    diederich300 = set()
    with open("/home/microbeta/crim/FastBridge/FastBridgeApp/Bridge_Latin_List_Diederich_all_prep_fastbridge_7_2020_BridgeImport.csv", 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        count = 0
        for row in reader:
            if count <= 306:  # From Latin vocabulary knowledge and the Readability of Latin texts
                diederich300.add(row['TITLE'])
                count += 1
            else:
                break

    dcc = create_word_set(
        "/home/microbeta/crim/FastBridge/FastBridgeApp/Bridge-Vocab-Latin-List-DCC.csv")

    diederich1500 = create_word_set(
        "/home/microbeta/crim/FastBridge/FastBridgeApp/Bridge_Latin_List_Diederich_all_prep_fastbridge_7_2020_BridgeImport.csv")

    # Stats boilerplate
    start_index = text_object.sections[start_section]
    end_index = text_object.sections[end_section]
    text_slice = text_object.words[start_index:end_index]

    if start_section == 'start' and end_section == 'end':
        text_slice = text_object.words

    # Bad naming standards, these are counting which words are NOT in these lists
    in300 = 0
    inDCC = 0
    in1500 = 0
    countWords = 0
    for word_tuple in text_slice:
        if word_tuple[0] not in diederich300:
            in300 += 1
        if word_tuple[0] not in dcc:
            inDCC += 1
        if word_tuple[0] not in diederich1500:
            in1500 += 1
        countWords += 1

    freq300 = in300/countWords
    freqDCC = inDCC/countWords
    freq1500 = in1500/countWords

    mean_word_length = get_avg_word_length(
        text_object, start_section, end_section)
    lexical_sophistication = get_lexical_sophistication(
        text_object, start_section, end_section)

    lexical_variation = get_lexical_variation(
        text_object, start_section, end_section)
    logTTR = lexical_variation[3]
    rootTTR = lexical_variation[1]

    lex_r = ((mean_word_length*0.457)+(freq300*0.063)+(freqDCC*0.076)+(freq1500 *
             0.092)+(lexical_sophistication*0.059)+(logTTR*0.312)+(rootTTR*0.143))

    lex_r -= 11.7
    lex_r *= 0.833

    return lex_r


def plot_cum_lex_load(text_object: Text, start_section, end_section):
    start_index = text_object.sections[start_section]
    end_index = text_object.sections[end_section]
    text_slice = text_object.words[start_index:end_index]

    if start_section == 'start' and end_section == 'end':
        text_slice = text_object.words

    # Go through the words of text_slice
    # Connect to Dictionary to filter out PROPER, "1" and "T"
    words = []
    scores = []
    for word_tuple in text_slice:
        word = word_tuple[0]
        # filter out proper nouns
        if word in latin_dict and latin_dict[word]["PROPER"] not in ["1", "T"]:
            words.append(word)

    for word in words:
        if word in latin_dict:
            if int(latin_dict[word]["CORPUSFREQ"]) <= 200:
                scores.append(2)
                continue
            if int(latin_dict[word]["CORPUSFREQ"]) > 200 and int(latin_dict[word]["CORPUSFREQ"]) <= 1000:
                scores.append(1)
                continue
            if int(latin_dict[word]["CORPUSFREQ"]) > 1000 and int(latin_dict[word]["CORPUSFREQ"]) <= 2000:
                scores.append(-1)
                continue
            if int(latin_dict[word]["CORPUSFREQ"]) > 2000 and int(latin_dict[word]["CORPUSFREQ"]) <= 5000:
                scores.append(-2)
                continue
            if int(latin_dict[word]["CORPUSFREQ"]) > 5000:
                scores.append(-4)
                continue
        else:
            scores.append(-4)
            continue

    cumulative_scores = np.cumsum(scores)

    # Calculate rolling average
    # rolling_average = pd.Series(cumulative_scores).rolling(window=rolling_window_size).mean()

    x_indexes = list(range(len(words)))

    sns.set_style("ticks")
    sns.set_context("paper")
    plt.figure(figsize=(10, 5))
    sns.lineplot(x=x_indexes, y=cumulative_scores,
                 errorbar=None, color=colorblind_palette[0])
    sns.despine()
    plt.title(f"Cumulative Lexical Load of {text_object.name}", **title_font)
    plt.xlabel('Word', **axis_font)
    plt.ylabel('Cumulative Lexical Load Score', **axis_font)

    # Get the current Axes instance
    ax = plt.gca()

    # set font properties to x and y tick labels
    plt.setp(ax.get_xticklabels(), fontproperties=prop)
    plt.setp(ax.get_yticklabels(), fontproperties=prop)

    plt.show()


def plot_rolling_lin_lex_load(text_object: Text, start_section, end_section, rolling_window_size=25):
    start_index = text_object.sections[start_section]
    end_index = text_object.sections[end_section]
    text_slice = text_object.words[start_index:end_index]

    if start_section == 'start' and end_section == 'end':
        text_slice = text_object.words

    # Go through the words of text_slice
    # Connect to Dictionary to filter out PROPER, "1" and "T"
    words = []
    scores = []
    for word_tuple in text_slice:
        word = word_tuple[0]
        # filter out proper nouns
        if word in latin_dict and latin_dict[word]["PROPER"] not in ["1", "T"]:
            words.append(word)

    for word in words:
        if word in latin_dict:
            if int(latin_dict[word]["CORPUSFREQ"]) <= 200:
                scores.append(2)
                continue
            if int(latin_dict[word]["CORPUSFREQ"]) > 200 and int(latin_dict[word]["CORPUSFREQ"]) <= 1000:
                scores.append(1)
                continue
            if int(latin_dict[word]["CORPUSFREQ"]) > 1000 and int(latin_dict[word]["CORPUSFREQ"]) <= 2000:
                scores.append(-1)
                continue
            if int(latin_dict[word]["CORPUSFREQ"]) > 2000 and int(latin_dict[word]["CORPUSFREQ"]) <= 5000:
                scores.append(-2)
                continue
            if int(latin_dict[word]["CORPUSFREQ"]) > 5000:
                scores.append(-4)
                continue
        else:
            scores.append(-4)
            continue

    # Calculate rolling average of the scores
    rolling_average = pd.Series(scores).rolling(
        window=rolling_window_size).mean()

    # Apply Savitzky-Golay filter
    # window size 51, polynomial order 3
    smoothed_scores = savgol_filter(rolling_average, 101, 3)

    x_indexes = list(range(len(words)))

    # calculate average linear lexical score for the entire text
    average_score = np.mean(scores)

    sns.set_style("ticks")
    sns.set_context("paper")
    plt.figure(figsize=(10, 5))
    sns.lineplot(x=x_indexes, y=smoothed_scores,
                 errorbar=None, color=colorblind_palette[0])

    # add a horizontal line representing the average linear lexical score
    plt.axhline(y=average_score, color=colorblind_palette[1], linestyle='--')

    sns.despine()
    plt.title(f"Linear Lexical Load of {text_object.name}", **title_font)
    plt.xlabel('Word', **axis_font)
    plt.ylabel(
        f'{rolling_window_size}-Word Rolling Average of Linear Lexical Load Score', **axis_font)

    # Get the current Axes instance
    ax = plt.gca()

    # set x-axis ticks to window size?  -> Only activate this if you want to see all the numbers jumble up at the bottom
    # tick_spacing = rolling_window_size  # change this to the size of your slices
    # ax.xaxis.set_major_locator(ticker.MultipleLocator(tick_spacing))

    # set font properties to x and y tick labels
    plt.setp(ax.get_xticklabels(), fontproperties=prop)
    plt.setp(ax.get_yticklabels(), fontproperties=prop)

    plt.show()


def plot_linear_heatmap(text_object: Text, start_section, end_section, slice_divisor=25, slice_override=0):
    start_index = text_object.sections[start_section]
    end_index = text_object.sections[end_section]
    text_slice = text_object.words[start_index:end_index]

    if start_section == 'start' and end_section == 'end':
        text_slice = text_object.words

    # Go through the words of text_slice
    # Connect to Dictionary to filter out PROPER, "1" and "T"
    words = []
    scores = []
    for word_tuple in text_slice:
        word = word_tuple[0]
        # filter out proper nouns
        if word in latin_dict and latin_dict[word]["PROPER"] not in ["1", "T"]:
            words.append(word)

    for word in words:
        if word in latin_dict:
            if int(latin_dict[word]["CORPUSFREQ"]) <= 200:
                scores.append(2)
                continue
            if int(latin_dict[word]["CORPUSFREQ"]) > 200 and int(latin_dict[word]["CORPUSFREQ"]) <= 1000:
                scores.append(1)
                continue
            if int(latin_dict[word]["CORPUSFREQ"]) > 1000 and int(latin_dict[word]["CORPUSFREQ"]) <= 2000:
                scores.append(-1)
                continue
            if int(latin_dict[word]["CORPUSFREQ"]) > 2000 and int(latin_dict[word]["CORPUSFREQ"]) <= 5000:
                scores.append(-2)
                continue
            if int(latin_dict[word]["CORPUSFREQ"]) > 5000:
                scores.append(-4)
                continue
        else:
            scores.append(-4)
            continue

    # Convert scores to an array of floats->FOR PADDING
    scores = np.array(scores, dtype=float)

    slice_size = len(scores)//slice_divisor

    if slice_override != 0:
        slice_size = slice_override

    # Calculate the remainder of the division
    remainder = len(scores) % slice_size

    # If there's a remainder, pad the scores array
    if remainder != 0:
        # Calculate how many elements we need to add
        pad_size = slice_size - remainder

    # Pad the scores array with np.nan values
    scores = np.pad(scores, (0, pad_size), mode='constant',
                    constant_values=np.nan)

    # Reshape the scores into 2D array where each row corresponds to a slice of words
    scores_matrix = np.array(scores).reshape((-1, slice_size))

    sns.set_style("ticks")
    sns.set_context("paper")
    plt.figure(figsize=(10, 5))

    # Create a heatmap
    sns.heatmap(scores_matrix, cmap='cividis')

    sns.despine()
    plt.title(
        f"Heatmap of Linear Lexical Load of {text_object.name}", **title_font)
    plt.xlabel('Word within Word Slice', **axis_font)
    plt.ylabel(f'{slice_size}-Word Slice', **axis_font)

    # calculate average linear lexical score for the entire text
    average_score = np.mean(scores)

    # Get the current Axes instance
    ax = plt.gca()

    # set font properties to x and y tick labels
    plt.setp(ax.get_xticklabels(), fontproperties=prop)
    plt.setp(ax.get_yticklabels(), fontproperties=prop)

    plt.show()


# Routing
router = APIRouter()
router_path = Path.cwd()
templates = Jinja2Templates(directory="templates")
"""Expected Prefix: /stats"""

selected_texts = []


@router.get("/")
async def stats_index(request: Request):
    return templates.TemplateResponse("stats-list-index.html", {"request": request})


@router.get("/{language}/")
async def stats_select(request: Request, language: str):
    return templates.TemplateResponse("stats_select.html", {"request": request, "titles": DefinitionTools.render_titles(language), 'titles2': DefinitionTools.render_titles(language, "2")})
    # return templates.TemplateResponse("select.html", {"request": request, "titles": DefinitionTools.render_titles(language), 'titles2': DefinitionTools.render_titles(language, "2") })


@router.get("/select/sections/{textname}/{language}/")
async def stats_select_section(request: Request, textname: str, language: str):
    print("reaching section endpoint")
    sectionDict = DefinitionTools.get_sections(language)
    sectionBook = sectionDict[textname]
    return sectionBook


@router.post("/{language}/result/{sourcetexts}/{starts}-{ends}/{running_list}/")
@router.get("/{language}/result/{sourcetexts}/{starts}-{ends}/{running_list}/")
async def stats_simple_result(request: Request, starts: str, ends: str, sourcetexts: str, language: str, running_list: str):
    context = {"request": request}
    if running_list == "running":
        running_list = True
    else:
        running_list = False

    if language == "Latin":
        dictionary_path = "/home/microbeta/crim/FastBridge/FastBridgeApp/bridge_latin_dictionary.csv"
        diederich_path = "/home/microbeta/crim/FastBridge/FastBridgeApp/Bridge_Latin_List_Diederich_all_prep_fastbridge_7_2020_BridgeImport.csv"
        dcc_path = "/home/microbeta/crim/FastBridge/FastBridgeApp/Bridge-Vocab-Latin-List-DCC.csv"
        analyzer = TextAnalyzer(dictionary_path, diederich_path, dcc_path)
    else:  # Greek -> Change this when you put in the Greek files
        analyzer = TextAnalyzer("FastBridgeApp\\bridge_latin_dictionary.csv",
                                "FastBridgeApp\Bridge_Latin_List_Diederich_all_prep_fastbridge_7_2020_BridgeImport.csv", "FastBridgeApp\Bridge-Vocab-Latin-List-DCC.csv")

    if '+' not in sourcetexts:#Only 1 text has been added
        analyzer.add_text(sourcetexts, language, starts, ends)

        print(str(analyzer))

        textname = analyzer.get_textname()
        word_count = analyzer.num_words()
        vocab_size = analyzer.vocab_size()
        hapax, hapax_percentage = analyzer.hapax_legonema()
        lex_dens = analyzer.lex_density()
        lex_sophistication = analyzer.lex_sophistication()
        lex_variation = analyzer.lex_variation()
        lex_r = analyzer.LexR()
        total_words_no_p = analyzer.totalWordsNoProper()
        unique_words_no_p = analyzer.uniqueWordsNoProper()
        avgWordLength = analyzer.avgWordLength()
        top20NoDie300 = analyzer.top20NoDie300()
        freqBin1,freqBin2,freqBin3,freqBin4,freqBin5,freqBin6 = analyzer.freqBinMetrics()

        # plot functions return the location of plot images
        freq_plot_path = analyzer.plot_word_freq()  # call your plot function here
        freq_relative_plot_path = os.path.relpath(
            freq_plot_path, start='/home/microbeta/crim/FastBridge/FastBridgeApp/static/assets/plots/')

        cum_lex_plot_path = analyzer.plot_cum_lex_load()
        cum_lex_relative_plot_path = os.path.relpath(
            cum_lex_plot_path, start='/home/microbeta/crim/FastBridge/FastBridgeApp/static/assets/plots/')

        lin_lex_plot_path = analyzer.plot_lin_lex_load()
        lin_lex_relative_plot_path = os.path.relpath(
            lin_lex_plot_path, start='/home/microbeta/crim/FastBridge/FastBridgeApp/static/assets/plots/')

        freq_bins_plot_path = analyzer.plot_freq_bin()
        freq_bins_relative_plot_path = os.path.relpath(
            freq_bins_plot_path, start='/home/microbeta/crim/FastBridge/FastBridgeApp/static/assets/plots/'
        )

        context.update({
            "request": request,
            "text_name": textname,
            "start_section": starts,
            "end_section": ends,
            "word_count": word_count,
            "vocab_size": vocab_size,
            "hapax_legonema": hapax,
            "hapax_percentage": hapax_percentage,
            "lexical_density": lex_dens,
            "lexical_sophistication": lex_sophistication,
            "lexical_variation": lex_variation,
            "LexR": lex_r,
            "total_words_no_proper": total_words_no_p,
            "unique_words_no_proper": unique_words_no_p,
            "avg_word_length": avgWordLength,
            "top20_NoDie300":top20NoDie300,
            "freq1":freqBin1,
            "freq2":freqBin2,
            "freq3": freqBin3,
            "freq4": freqBin4,
            "freq5":freqBin5,
            "freq6":freqBin6,
            "freq_plot_path": freq_relative_plot_path,
            "cum_lex_plot_path": cum_lex_relative_plot_path,
            "lin_lex_plot_path": lin_lex_relative_plot_path,
            "freq_bins_plot_path": freq_bins_relative_plot_path
        })
        print(f"freq rel path: {freq_relative_plot_path}")
        print(f"cum lex rel path: {cum_lex_relative_plot_path}")
        print(f"lin lex rel path: {lin_lex_relative_plot_path}")
        print(f"freq bins rel path: {freq_bins_relative_plot_path}")
        return templates.TemplateResponse("stats-single-text.html", context)
    else:#multiple texts have been added

        #Get text information from URL
        analyzer_texts = sourcetexts.split('+')
        analyzer_starts = starts.split('+')
        analyzer_ends = ends.split('+')

        #Add text info to analyzer
        analyzers = []
        for i in range(len(analyzer_texts)):
            if language == "Latin":
                dictionary_path = "/home/microbeta/crim/FastBridge/FastBridgeApp/bridge_latin_dictionary.csv"
                diederich_path = "/home/microbeta/crim/FastBridge/FastBridgeApp/Bridge_Latin_List_Diederich_all_prep_fastbridge_7_2020_BridgeImport.csv"
                dcc_path = "/home/microbeta/crim/FastBridge/FastBridgeApp/Bridge-Vocab-Latin-List-DCC.csv"
                analyzer = TextAnalyzer(dictionary_path, diederich_path, dcc_path)
            analyzer.add_text(analyzer_texts[i],language, analyzer_starts[i], analyzer_ends[i])
        
        #Used multiple TextAnalyzer's, account for dynamicism here

        # Getting Metrics, Hapax
        text_names = [a.texts[0][0] for a in analyzers] 
        text_starts = [a.texts[0][1] for a in analyzers]
        text_ends = [a.texts[0][2] for a in analyzers]
        word_counts = [a.num_words() for a in analyzers]
        vocab_sizes = [a.vocab_size() for a in analyzers]
        hapaxes_and_percentages = [a.hapax_legonema(tupleFlag=True) for a in analyzers]#(hapaxes[], percent_hapax)
        # hapaxes, hapax_percentages = zip(*[a.hapax_legonema() for a in analyzers])
        lex_densities = [a.lex_density() for a in analyzers]
        lex_sophists = [a.lex_sophistication() for a in analyzers]
        lex_variations = [a.lex_variation() for a in analyzers]
        lex_rs = [a.LexR() for a in analyzers]
        no_p_word_counts = [a.totalWordsNoProper() for a in analyzers]
        no_p_vocab_sizes = [a.uniqueWordsNoProper() for a in analyzers]
        avg_word_lengths = [a.avgWordLength() for a in analyzers]
        characteristic_words = [a.top20NoDie300() for a in analyzers]
        freq_bins = [a.freqBinMetrics() for a in analyzers]#(freq1,freq2,freq3,freq4,freq5,freq6)

        #Getting Plots
        #we need to specify which plot path each plot will go to, use plot_num argument in each plot method
        word_freq_paths = [analyzers[i].plot_word_freq(plot_num = i) for i in range(len(analyzers))]
        cum_lex_plot_paths = [analyzers[i].plot_cum_lex_load(plot_num = i+len(analyzers)) for i in range(len(analyzers))]
        lin_lex_plot_paths = [analyzers[i].plot_lin_lex_load(plot_num = i+(2*len(analyzers))) for i in range(len(analyzers))]
        freq_bin_plot_paths = [analyzers[i].plot_freq_bin(plot_num = i+(3*len(analyzers))) for i in range(len(analyzers))]
        

        #add analyzer stats from each text to context
        context.update({
            "request": request,
            "textNames": text_names,
            "textStarts": text_starts,
            "textEnds": text_ends,
            "wordsCounts": word_counts,
            "vocabSizes": vocab_sizes,
            "hapaxes_and_percents": hapaxes_and_percentages,
            "lexDensities": lex_densities,
            "lexRs": lex_rs,
            "noPWordCounts": no_p_word_counts,
            "noPVocabSizes": no_p_vocab_sizes,
            "avgWordLengths": avg_word_lengths,
            "characteristicWords": characteristic_words,
            "freqBins": freq_bins,
            "wordFreqPaths": word_freq_paths,
            "cumLexPaths": cum_lex_plot_paths,
            "linLexPaths": lin_lex_plot_paths,
            "freqBinPaths": freq_bin_plot_paths
        })

        #Create stats-multiple-texts.html, 2 columns, 2 dropdown menus
        #

        return templates.TemplateResponse("stats-multiple-texts.html", context)

   
@router.get("/get_metrics/{index}")
async def get_metrics_html(request: Request, index: int):
    # Assuming `context` is a globally defined dictionary storing the data
    # Here, you would retrieve the metrics and plots for the given index from the context dictionary
    
    text_name = context['textNames'][index]
    text_start = context['textStarts'][index]
    text_end = context['textEnds'][index]
    word_count = context['wordsCounts'][index]
    vocab_size = context['vocabSizes'][index]
    hapax = context['hapaxes'][index]
    # ...and so on for each metric in the context dictionary

    # Then, you would render these to an HTML string using a new Jinja2 template
    # This new template should just contain the HTML for the metrics and plots
    return templates.TemplateResponse('metrics_and_plots.html', 
    {
        "request": request, 
        "textName": text_name, 
        "textStart": text_start, 
        "textEnd": text_end,
        "wordCount": word_count,
        "vocabSize": vocab_size,
        "hapax": hapax,
        # ...and so on for each metric in the context dictionary
    })


@router.get("/formulas")
async def read_formulas(request: Request):
    return templates.TemplateResponse("stats-formulas.html", {"request": request})


@router.get("/cumulative/{language}/")
async def stats_cumulative(request: Request, language: str):
    # Retrieve the selected text names from the session or storage
    # Replace with your storage retrieval logic
    selected_texts = retrieve_selected_texts()

    # Process the selected text names and retrieve the corresponding book data
    sectionDict = DefinitionTools.get_sections(language)
    sectionBooks = [sectionDict[textname] for textname in selected_texts]

    # Perform cumulative statistics calculations or any other operations on sectionBooks

    return templates.TemplateResponse("stats_cumulative.html", {"request": request, "sectionBooks": sectionBooks})


# main()
# empty = LatinTextAnalyzer("FastBridgeApp\\bridge_latin_dictionary.csv","FastBridgeApp\Bridge_Latin_List_Diederich_all_prep_fastbridge_7_2020_BridgeImport.csv","FastBridgeApp\Bridge-Vocab-Latin-List-DCC.csv")

# whole = TextAnalyzer("FastBridgeApp\\bridge_latin_dictionary.csv","FastBridgeApp\Bridge_Latin_List_Diederich_all_prep_fastbridge_7_2020_BridgeImport.csv","FastBridgeApp\Bridge-Vocab-Latin-List-DCC.csv")
# whole.add_text('vergil_aeneid_ap_selections', 'Latin', "start", "end")
# print(str(whole))
# partsOfWhole = LatinTextAnalyzer("FastBridgeApp\\bridge_latin_dictionary.csv","FastBridgeApp\Bridge_Latin_List_Diederich_all_prep_fastbridge_7_2020_BridgeImport.csv","FastBridgeApp\Bridge-Vocab-Latin-List-DCC.csv")
# partsOfWhole.add_text('vergil_aeneid_ap_selections', 'Latin', "1.1", "1.436")
# partsOfWhole.add_text('vergil_aeneid_ap_selections', 'Latin', "1.436", "6.899")

# print(str(empty))
# pause = input()


# pause2 = input()
# print(str(partsOfWhole))


# Using the get_text function to load the text instance
# text_instance = get_text('vergil_aeneid_ap_selections', 'Latin').book

# section_start = "1.1"
# section_end = "1.143"
# 4.355
# Call new functions
# print(f"\n\nStats for sections: {section_start} - {section_end}")
# print(f"Number of words:\t{get_number_of_words(text_instance, str(section_start), str(section_end))}")
# print(f"Vocabulary Size:\t{get_vocabulary_size(text_instance,str(section_start), str(section_end))}")
# print(f"Hapax Legomena: {get_hapax_legomena(text_instance, str(section_start), str(section_end))}")

# plot_avg_word_length(text_instance, str(section_start), str(section_end))
# plot_avg_word_length2(text_instance, '1.1', '6.899')
# plot_word_frequency(text_instance, str(section_start), str(section_end))


# print(f"Lexical Density:\t{get_lexical_density(text_instance, str(section_start), str(section_end))}")
# The density is way too slow

# print(f"Lexical Sophistication: {get_lexical_sophistication(text_instance,str(section_start), str(section_end))}")
# print(f"Lexical Variation: {get_lexical_variation(text_instance, str(section_start), str(section_end))}")
# print(f"Average Subordinations per Section/Sentence: {get_average_subordinations_per_section(1,1,4,355)}")

# print(f"LexR:\t\t{get_lex_r(text_instance, str(section_start), str(section_end))}")

# plot_cum_lex_load(text_instance, str(section_start), str(section_end))
# plot_rolling_lin_lex_load(text_instance, str(section_start), str(section_end))
# plot_linear_heatmap(text_instance, str(section_start), str(section_end), slice_override=30)
