import os
from math import log, sqrt
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px
from text import Text
from collections import defaultdict #comment
import matplotlib.font_manager as fm
import time
import numpy as np
from scipy.signal import savgol_filter

from pathlib import Path
from MongoDefinitionTools import db, dict_db, mg_get_locations, mg_get_text_as_Text


# Get the directory containing the current script.
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)#FastBridgeApp

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


@timer_decorator
def mg_get_latin_dictionary(db):
    word_dictionary = {}
    cursor = db.bridge_latin_dictionary.find()
    for row in cursor:
        if 'TITLE' in row:
            word_dictionary[row['TITLE']] = row
    return word_dictionary

@timer_decorator
def mg_get_dcc(db, collection_name):
    dcc = set()
    cursor = db[collection_name].find()
    for row in cursor:
        dcc.add(row['head_word'])
    return dcc

@timer_decorator
def mg_get_diederich(collection_name):
    diederich300 = set()
    diederich1500 = set()
    cursor = db[collection_name].find()
    for row in cursor:
        if row['counter'] <= 306:
            diederich300.add(row['head_word'])
        diederich1500.add(row['head_word'])
    return diederich300, diederich1500

# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$


# using memoization to cache results of get_slice
def get_slice_cached():
    cache = {}

    def inner(text_object: Text, start_section, end_section):
        key = (id(text_object), start_section, end_section)
        if key in cache:
            return cache[key]
        result = text_object.get_words(start_section, end_section, stats=True)
        cache[key] = result
        return result

    return inner

get_slice = get_slice_cached()


def find_hapax_legomena(words, dictionary:dict):
    word_frequencies = defaultdict(int)
    for word in words:
        if word and word in dictionary:
            if(dictionary[word]): word_frequencies[dictionary[word]['SIMPLE_LEMMA']] += 1
        elif word.upper() in dictionary:
            print(f"Using uppercase version for word '{word}'")
            word_frequencies[dictionary[word.upper()]['SIMPLE_LEMMA']] += 1
        else:
            print(f"Word '{word}' not found in dictionary, skipping.")
    return [word.capitalize() for word, freq in word_frequencies.items() if freq == 1 and word]


class TextAnalyzer:

    def __init__(self):

        self.texts = [] 
        self.num_words_ct = None
        
        self.dictionary, self.dictionary_time = mg_get_latin_dictionary(dict_db)
        print("Dictionary Loaded: {} seconds".format(self.dictionary_time))

        (result, self.diederich_time) = mg_get_diederich("Diederich Frequency List (General)_LIST")
        self.diederich300, self.diederich1500 = result

        self.dcc, self.dcc_time = mg_get_dcc(db, "DCC Latin Core_LOCAL_LIST")
        print("DCC Loaded: {} seconds".format(self.dcc_time))


    # Add working file for subordinations/section?
    def add_text(self, form_request: str, language: str, start_section, end_section):
        location_list, location_words = mg_get_locations(language, form_request, get_index=True)
        self.texts.append((mg_get_text_as_Text(language, form_request, location_list, location_words),start_section, end_section))

    def get_textname(self):
        if len(self.texts) == 0: return -1
        elif len(self.texts) == 1: return self.texts[0][0].name
        else: return " + ".join([text[0].name for text in self.texts])

    def num_words(self) -> int:
        if self.num_words_ct: return self.num_words_ct # no need to recompute every time
        if not self.texts: return -1

        total = 0
        for text in self.texts:
            text_slice = get_slice(text[0], text[1], text[2])
            # head_word is a guaranteed field so len(text_slice) should be sufficient
            total += len(text_slice) 
        
        self.num_words_ct = total
        return self.num_words_ct

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
    def hapax_legonema(self, tupleFlag=False):
        if not self.texts: return ([], 0)

        allwords = []
        for text in self.texts:
            text_slice = get_slice(text[0], text[1], text[2])
            for word_tuple in text_slice:
                word = word_tuple[0]
                if word:
                    allwords.append(word)

        if not allwords: return ([], 0)

        hapax_legomena = find_hapax_legomena(allwords, self.dictionary)
        hapax_legomena = sorted(hapax_legomena)
        percentage = len(hapax_legomena) / len(allwords) * 100

        return (hapax_legomena, percentage)

    @round_decorator
    def lex_density(self):
        lexical_categories = {"Adjective", "Adverb", "Noun", "Verb"}

        if not self.texts:
            return -1

        lexical_sum = 0
        for text in self.texts:
            text_slice = get_slice(text[0], text[1], text[2])
            for word_tuple in text_slice:
                word = word_tuple[0]
                if word in self.dictionary and self.dictionary[word]["PART_OF_SPEECH"] in lexical_categories:
                    lexical_sum += 1

        total_words = self.num_words()
        lexical_density = lexical_sum / total_words if total_words > 0 else 0
        return lexical_density

    @round_decorator
    def lex_sophistication(self):
        if len(self.texts) == 0:
            return -1

        rare_count = 0
        total_words = 0

        for text in self.texts:
            text_slice = get_slice(text[0], text[1], text[2])
            for word_tuple in text_slice:
                word = word_tuple[0]
                if word not in self.diederich1500:
                    rare_count += 1
                total_words += 1

        lexical_sophistication = rare_count / total_words if total_words > 0 else 0
        return lexical_sophistication

    @round_decorator
    def lex_variation(self):
        if len(self.texts) == 0:
            return -1

        all_words = []

        for text in self.texts:
            text_slice = get_slice(text[0], text[1], text[2])
            for word_tuple in text_slice:
                word = word_tuple[0]
                if word:  # skip empty/null words
                    all_words.append(word)

        total_words = len(all_words)
        num_unique = len(set(all_words))

        if total_words > 0 and num_unique > 0:
            TTR = num_unique / total_words
            RootTTR = num_unique / sqrt(total_words)
            CTTR = num_unique / sqrt(2 * total_words)
            LogTTR = log(num_unique) / log(total_words)
            return (TTR, RootTTR, CTTR, LogTTR)
        else:
            return (0, 0, 0, 0)

    @round_decorator
    def LexR(self):
        if len(self.texts) == 0:
            return 'NA'

        text_slice = get_slice(self.texts[0][0], self.texts[0][1], self.texts[0][2])

        out300 = 0
        outDCC = 0
        out1500 = 0
        countWords = 0

        for word_tuple in text_slice:
            word = word_tuple[0]
            if word not in self.diederich300:
                out300 += 1
            if word not in self.dcc:
                outDCC += 1
            if word not in self.diederich1500:
                out1500 += 1
            countWords += 1

        if countWords == 0:
            return 'NA'  # Avoid division by zero

        freq300 = (out300 / countWords) * 100
        freqDCC = (outDCC / countWords) * 100
        freq1500 = (out1500 / countWords) * 100

        mean_word_length = self.avgWordLength()
        lexical_sophistication = self.lex_sophistication()
        lexical_variation = self.lex_variation()
        logTTR = lexical_variation[3]
        rootTTR = lexical_variation[1]

        lex_r = ((mean_word_length * 0.457) + (freq300 * 0.063) + (freqDCC * 0.076) + (freq1500 * 0.092) +
                 (lexical_sophistication * 0.059) + (logTTR * 0.312) + (rootTTR * 0.143))

        lex_r -= 11.7
        lex_r += 6
        lex_r *= 0.833

        return lex_r

    def totalWordsNoProper(self):
        if len(self.texts) == 0:
            return -1

        words = []

        for text in self.texts:
            text_slice = get_slice(text[0], text[1], text[2])
            for word_tuple in text_slice:
                word = word_tuple[0]
                # filter out proper nouns
                if word in self.dictionary and self.dictionary[word]["PROPER"] not in ["1", "T"]:
                    words.append(word)

        return len(words)

    def uniqueWordsNoProper(self):
        if len(self.texts) == 0:
            return -1

        vocabulary = set()

        for text in self.texts:
            text_slice = get_slice(text[0], text[1], text[2])
            for word_tuple in text_slice:
                word = word_tuple[0]
                if word in self.dictionary and self.dictionary[word]["PROPER"] not in ["1", "T"]:
                    vocabulary.add(word)

        return len(vocabulary)

    def top20NoDie300(self):
        properNounCats = ["1", "T"]
        if len(self.texts) == 0:
            return -1

        word_counts = defaultdict(int)

        for text in self.texts: # adapted to work for multi text
            text_slice = get_slice(text[0], text[1], text[2])
            for word_tuple in text_slice:
                word = word_tuple[0] # head_word
                if word in self.dictionary:
                    word_info = self.dictionary[word]
                    if not word_info["CORPUSFREQ"]: continue
                    if word_info["PROPER"] not in properNounCats and int(word_info["CORPUSFREQ"]) > 300:
                        lemma = word_info.get("SIMPLE_LEMMA")
                        if lemma: word_counts[lemma] += 1

        top_20_words = sorted(word_counts.items(), key=lambda x: x[1], reverse=True)[:20]
        return [word for word, freq in top_20_words]

    @round_decorator
    def freqBinMetrics(self):
        if not self.texts:
            return -1

        words = []

        # Process all texts
        for text_data in self.texts:
            text_obj, start, end = text_data
            text_slice = get_slice(text_obj, start, end)

            for word_tuple in text_slice:
                word = word_tuple[0]
                if word in self.dictionary and self.dictionary[word]["PROPER"] not in ["1", "T"]:
                    words.append(word)

        # Frequency bins
        bins = {"0_200": 0, "201_500": 0, "501_1000": 0, "1001_1500": 0, "1501_2500": 0, "2500_plus": 0}

        for word in words:
            if word in self.dictionary:
                try:
                    freq = float(self.dictionary[word]["CORPUSFREQ"])
                except (ValueError, TypeError):
                    continue  # skip malformed frequencies

                if freq <= 200:
                    bins["0_200"] += 1
                elif freq <= 500:
                    bins["201_500"] += 1
                elif freq <= 1000:
                    bins["501_1000"] += 1
                elif freq <= 1500:
                    bins["1001_1500"] += 1
                elif freq <= 2500:
                    bins["1501_2500"] += 1
                else:
                    bins["2500_plus"] += 1

        total_words = len(words)
        if total_words == 0:
            return 0, 0, 0, 0, 0, 0

        return tuple(
            (count / total_words) * 100 for count in [
                bins["0_200"],
                bins["201_500"],
                bins["501_1000"],
                bins["1001_1500"],
                bins["1501_2500"],
                bins["2500_plus"]
            ]
        )        

    @round_decorator
    def avgWordLength(self):
        if len(self.texts) == 0:
            return -1

        words = []
        for text in self.texts:
            text_slice = get_slice(text[0], text[1], text[2])
            words.extend(word_tuple[0] for word_tuple in text_slice)

        if len(words) > 0: return sum(len(word) for word in words) / len(words)
        else: return 'NA'

    def plot_word_freq(self, plot_num=0):
        if len(self.texts) == 0:
            return
        
        text_slices_concat = []
        for text in self.texts:
            text_slices_concat += get_slice(text[0], text[1], text[2])
        
        # Create DataFrame
        df = pd.DataFrame(text_slices_concat, columns=[
            "Word", "Index", "Lemma", "Definition", "Notes", "Section", 
            "Word Count", "Sentence", "Case", "Lasla_Subordination_Code", "Grammatical_Subcategory"
        ])
        
        # Calculate word frequency
        word_frequency = df['Word'].value_counts().reset_index()
        word_frequency.columns = ['Word', 'Frequency']
        
        # Plot setup
        sns.set_style("ticks")
        sns.set_context("paper")
        plt.figure(figsize=(10, 5))
        sns.barplot(data=word_frequency[:30], x='Word', y='Frequency', palette=colorblind_palette)
        sns.despine()
        
        title = f"Word Frequency of {self.get_textname()}"
        plt.title(title, **title_font)
        
        plt.xlabel('Word', **axis_font)
        plt.ylabel('Frequency', **axis_font)
        plt.xticks(rotation=90)
        
        ax = plt.gca()
        plt.setp(ax.get_xticklabels(), fontproperties=prop)
        plt.setp(ax.get_yticklabels(), fontproperties=prop)
        
        # Save path
        plot_partial = f'static/assets/plots/plot{plot_num}.png'
        plot_path = parent_dir + plot_partial
        
        
        plt.tight_layout()
        plt.savefig(plot_partial)
        plt.close()
        
        # Return a relative path suitable for front-end use
        return f'/plot{plot_num}.png'

    def plot_lin_lex_load(self, plot_num=2):
        if len(self.texts) == 0:
            return "/blank_plot.png"

        # Gather all word tuples from all texts
        text_slices_concat = []
        for text in self.texts:
            text_slices_concat += get_slice(text[0], text[1], text[2])

        # Save actual text locations (e.g. "1.2", "3.5", etc.)
        x_labels_full = [word_tuple[5].replace('_', '.') for word_tuple in text_slices_concat]

        scores = []
        for word_tuple in text_slices_concat:
            word = word_tuple[0]
            if word in self.dictionary:
                freq = self.dictionary[word]["CORPUSFREQ"]
                if not freq:
                    continue
                if freq <= 200:
                    scores.append(2)
                elif 200 < freq <= 1000:
                    scores.append(1)
                elif 1000 < freq <= 2000:
                    scores.append(-1)
                elif 2000 < freq <= 5000:
                    scores.append(-2)
                elif freq > 5000:
                    scores.append(-4)
            else:
                scores.append(-4)

        if len(scores) == 0:
            return "/blank_plot.png"

        rolling_window_size = 25
        rolling_average = pd.Series(scores).rolling(window=rolling_window_size).mean()
        rolling_average.dropna(inplace=True)

        savgol_num = min(51, len(rolling_average))
        if savgol_num % 2 == 0:
            savgol_num -= 1
        if savgol_num <= 3:
            return "/blank_plot.png"

        smoothed_scores = savgol_filter(rolling_average, savgol_num, 3)

        x_numeric = list(range(len(smoothed_scores)))

        sns.set_style("ticks")
        sns.set_context("paper")
        plt.figure(figsize=(10, 5))
        sns.lineplot(x=x_numeric, y=smoothed_scores, color=colorblind_palette[0])
        sns.despine()

        # Replace numeric ticks with real word locations (sampled)
        x_labels_trimmed = x_labels_full[rolling_window_size - 1:]  # match length after rolling
        num_ticks = 10
        tick_indices = np.linspace(0, len(x_numeric) - 1, num_ticks, dtype=int)
        tick_locations = [x_numeric[i] for i in tick_indices]
        tick_labels = [str(x_labels_trimmed[i]) for i in tick_indices]

        plt.xticks(tick_locations, tick_labels, rotation=45, ha='right')

        if len(self.texts) == 1:
            title = f"Rolling Linear Lexical Load of {self.texts[0][0].name}"
        else:
            title = f"Rolling Linear Lexical Load of {self.get_textname()}"
        plt.title(title, **title_font)

        plt.xlabel('Text Location', **axis_font)
        plt.ylabel('Smoothed Lexical Load', **axis_font)

        plt.tight_layout()

        plot_partial = f'static/assets/plots/plot{plot_num}.png'
        plot_path = parent_dir + plot_partial
        plt.savefig(plot_partial)
        plt.close()

        return f'/plot{plot_num}.png'


    def plot_cum_lex_load(self, plot_num=1):
        if len(self.texts) == 0:
            return '/blank_plot.png'

        # Combine all slices to support multi-text
        text_slices_concat = []
        for text in self.texts:
            text_slices_concat += get_slice(text[0], text[1], text[2])

        # Actual x labels (e.g. word locations like '1.3' or '2.5')
        x_labels = [word_tuple[5].replace('_', '.') for word_tuple in text_slices_concat]

        scores = []
        for word_tuple in text_slices_concat:
            word = word_tuple[0]
            if word in self.dictionary:
                freq = self.dictionary[word]["CORPUSFREQ"]
                if not freq:
                    continue
                if freq <= 200:
                    scores.append(2)
                elif 200 < freq <= 1000:
                    scores.append(1)
                elif 1000 < freq <= 2000:
                    scores.append(-1)
                elif 2000 < freq <= 5000:
                    scores.append(-2)
                else:
                    scores.append(-4)
            else:
                scores.append(-4)

        if len(scores) == 0:
            return '/blank_plot.png'

        # Adjust scores by average to flatten baseline
        average_score = sum(scores) / len(scores)
        adjusted_scores = [score - average_score for score in scores]
        cumulative_scores = pd.Series(adjusted_scores).cumsum()

        # Numeric x positions for plotting
        x_numeric = list(range(len(cumulative_scores)))

        sns.set_style("ticks")
        sns.set_context("paper")
        plt.figure(figsize=(10, 5))
        sns.lineplot(x=x_numeric, y=cumulative_scores, color='blue')

        # Replace numeric ticks with real word location labels
        num_ticks = 10  # adjust this as needed
        tick_indices = np.linspace(0, len(x_numeric) - 1, num_ticks, dtype=int)
        tick_locations = [x_numeric[i] for i in tick_indices]
        tick_labels = [str(x_labels[i]) for i in tick_indices]  # ensure strings

        plt.xticks(tick_locations, tick_labels, rotation=45, ha='right')

        sns.despine()
        title = f"Cumulative Lexical Load of {self.get_textname()}"
        plt.title(title, fontdict={'fontsize': 12})
        plt.xlabel('Text Location', fontdict={'fontsize': 10})
        plt.ylabel('Cumulative Lexical Load', fontdict={'fontsize': 10})

        plot_partial = f'static/assets/plots/plot{plot_num}.png'
        plot_path = parent_dir + plot_partial

        plt.tight_layout()
        plt.savefig(plot_partial)
        plt.close()

        return f'/plot{plot_num}.png'


    def plot_freq_bin(self, plot_num=3):
        if len(self.texts) == 0:
            return '/blank_plot.png'

        # Gather words from all text slices
        words = []
        for text in self.texts:
            text_slice = get_slice(text[0], text[1], text[2])
            for word_tuple in text_slice:
                word = word_tuple[0]
                # filter out proper nouns
                if word in self.dictionary and self.dictionary[word]["PROPER"] not in ["1", "T"]:
                    words.append(word)

        if not words:
            return '/blank_plot.png'

        # Initialize frequency bins
        count0_200 = 0
        count201_500 = 0
        count501_1000 = 0
        count1001_1500 = 0
        count1501_2500 = 0
        count2500plus = 0

        for word in words:
            if word in self.dictionary:
                freq = self.dictionary[word]["CORPUSFREQ"]
                if not freq: continue
                if freq <= 200:
                    count0_200 += 1
                elif freq <= 500:
                    count201_500 += 1
                elif freq <= 1000:
                    count501_1000 += 1
                elif freq <= 1500:
                    count1001_1500 += 1
                elif freq <= 2500:
                    count1501_2500 += 1
                else:
                    count2500plus += 1

        total = len(words)
        data = {
            'Frequency Range': ['0-200', '201-500', '501-1000', '1001-1500', '1501-2500', '2500+'],
            'Percentage of Words': [
                count0_200 / total,
                count201_500 / total,
                count501_1000 / total,
                count1001_1500 / total,
                count1501_2500 / total,
                count2500plus / total
            ]
        }

        df = pd.DataFrame(data)

        sns.set_style("ticks")
        sns.set_context("paper")
        plt.figure(figsize=(10, 5))
        barplot = sns.barplot(x='Frequency Range', y='Percentage of Words', data=df, palette=colorblind_palette)
        sns.despine()

        title = f"Percentage of Words in Frequency Ranges of {self.get_textname()}" if len(self.texts) > 1 else f"Percentage of Words in Frequency Ranges of {self.texts[0][0].name}"
        plt.title(title, **title_font)

        plt.xlabel('Frequency Range', **axis_font)
        plt.ylabel('Percentage of Words', **axis_font)

        # Tick label fonts
        ax = plt.gca()
        plt.setp(ax.get_xticklabels(), fontproperties=prop)
        plt.setp(ax.get_yticklabels(), fontproperties=prop)

        # Annotate bars
        for p in barplot.patches:
            barplot.annotate(f"{p.get_height():.2f}",
                            (p.get_x() + p.get_width() / 2., p.get_height()),
                            ha='center', va='center',
                            xytext=(0, 10),
                            textcoords='offset points')

        # Save and return path
        plot_partial = f'static/assets/plots/plot{plot_num}.png'
        plot_path = parent_dir + plot_partial

        plt.tight_layout()
        plt.savefig(plot_partial)
        plt.close()

        return f'/plot{plot_num}.png'

    def _flatten_texts(self):
        text_slice = []
        for text in self.texts:
            text_slice.extend(get_slice(text[0], text[1], text[2]))
        return text_slice
    
    @round_decorator
    def spache_score(self):
        if len(self.texts) == 0:
            return 'NA'

        sections = set()
        total_words = 0
        unique_words = set()
        unfamiliar_words = set()

        for text in self.texts:
            text_slice = get_slice(text[0], text[1], text[2])
            for word in text_slice:
                lemma = word[0]
                section = word[7]
                if section is not None:
                    sections.add(section)
                total_words += 1
                unique_words.add(lemma)
                if lemma not in self.dcc:
                    unfamiliar_words.add(lemma)

        if len(sections) <= 1:
            return 'NA'
        avg_sentence_length = total_words / len(sections)
        percent_unfamiliar = (len(unfamiliar_words) / len(unique_words)) * 100

        spache_score = (0.121 * avg_sentence_length) + (0.082 * percent_unfamiliar) + 0.659
        return spache_score

    @round_decorator
    def dale_chall_score(self):
        if len(self.texts) == 0:
            return 'NA', 'NA'

        total_words = 0
        difficult_words = 0
        sections = set()

        for text in self.texts:
            text_slice = get_slice(text[0], text[1], text[2])
            for word in text_slice:
                lemma = word[0]
                section = word[7]

                total_words += 1
                if section is not None:
                    sections.add(section)

                if lemma not in self.dcc:
                    difficult_words += 1

        if len(sections) <= 1:
            return 'NA', 'NA'

        # Compute PDW and ASL
        pdw = (difficult_words / total_words) * 100
        asl = total_words / len(sections)

        # Dale-Chall formula
        score = (0.1579 * pdw) + (0.0496 * asl)
        if pdw >= 5:
            score += 3.6365
        new_dale_chall = 64 - (0.95*pdw) - (0.69*asl)
        
        return score, new_dale_chall
    
    @round_decorator
    def ari_score(self):
        if len(self.texts) == 0:
            return 'NA'

        total_words = 0
        total_chars = 0
        sections = set()

        for text in self.texts:
            text_slice = get_slice(text[0], text[1], text[2])
            for word in text_slice:
                lemma = word[0]
                section = word[7]

                total_words += 1
                total_chars += len(lemma)

                if section is not None:
                    sections.add(section)
        if len(sections) <= 1 or total_words == 0:
            return 'NA'

        sentence_count = len(sections)

        # ARI formula
        score = (4.71 * (total_chars / total_words)) + (0.5 * (total_words / sentence_count)) - 21.43
        return score

    @round_decorator
    def coleman_liau_score(self):
        if not self.texts:
            return 'NA'

        text_slice = self._flatten_texts()
        total_words = 0
        total_letters = 0
        sentence_sections = set()

        for word in text_slice:
            orthographic_form = word[2]
            section = word[7]

            if orthographic_form:
                total_words += 1
                total_letters += len(orthographic_form)

            if section is not None:
                sentence_sections.add(section)

        if total_words < 1:
            return 'NA'

        L = (total_letters / total_words) * 100  # average letters per 100 words
        S = (len(sentence_sections) / total_words) * 100  # average sentences per 100 words

        score = (0.0588 * L) - (0.296 * S) - 15.8
        return score


    def _get_word_stats(self, text_slice): # helper for lix and rix
        total_words = 0
        long_words = 0
        sentence_sections = set()

        for word in text_slice:
            orthographic_form = word[2]
            section = word[7]

            if orthographic_form:
                total_words += 1
                if len(orthographic_form) > 6: long_words += 1

            if section is not None: sentence_sections.add(section)

        return total_words, long_words, len(sentence_sections)

    @round_decorator
    def lix_score(self):
        if not self.texts:
            return 'NA'

        text_slice = self._flatten_texts()
        total_words, long_words, sentence_count = self._get_word_stats(text_slice)

        if total_words == 0 or sentence_count <= 1: return 'NA'

        percent_long_words = (long_words * 100) / total_words
        lix = (total_words / sentence_count) + percent_long_words
        
        return lix

    @round_decorator
    def rix_score(self):
        if not self.texts:
            return 'NA'

        text_slice = self._flatten_texts()
        _, long_words, sentence_count = self._get_word_stats(text_slice)

        if sentence_count <= 1:
            return 'NA'

        rix = long_words / sentence_count
        return rix

    @round_decorator
    def smog_score(self):
        if len(self.texts) == 0:
            return 'NA'

        text_slice = self._flatten_texts()

        complex_words = 0
        sentence_sections = set()

        for word in text_slice:
            orthographic_form = word[2]  # orthographic form
            section = word[7]            

            if orthographic_form and len(orthographic_form) > 6:
                complex_words += 1

            if section is not None:
                sentence_sections.add(section)

        sentence_count = len(sentence_sections)

        if sentence_count <= 1 or complex_words == 0:
            return 'NA'

        smog = 1.043 * sqrt((complex_words * 30) / sentence_count) + 3.1291
        return smog
    
    def plot_rolling_lin_lex_load(self, text_object: Text, start_section, end_section, rolling_window_size=25):
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
            if word in self.dictionary and self.dictionary[word]["PROPER"] not in ["1", "T"]:
                words.append(word)

        for word in words:
            if word in self.dictionary:
                if not self.dictionary[word]["CORPUSFREQ"]: continue
                if self.dictionary[word]["CORPUSFREQ"] <= 200:
                    scores.append(2)
                    continue
                if self.dictionary[word]["CORPUSFREQ"] > 200 and self.dictionary[word]["CORPUSFREQ"] <= 1000:
                    scores.append(1)
                    continue
                if self.dictionary[word]["CORPUSFREQ"] > 1000 and self.dictionary[word]["CORPUSFREQ"] <= 2000:
                    scores.append(-1)
                    continue
                if self.dictionary[word]["CORPUSFREQ"] > 2000 and self.dictionary[word]["CORPUSFREQ"] <= 5000:
                    scores.append(-2)
                    continue
                if self.dictionary[word]["CORPUSFREQ"] > 5000:
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

    def plot_linear_heatmap(self, text_object: Text, start_section, end_section, slice_divisor=25, slice_override=0):
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
            if word in self.dictionary and self.dictionary[word]["PROPER"] not in ["1", "T"]:
                words.append(word)

        for word in words:
            if word in self.dictionary:
                if not self.dictionary[word]["CORPUSFREQ"]: continue
                if self.dictionary[word]["CORPUSFREQ"] <= 200:
                    scores.append(2)
                    continue
                if self.dictionary[word]["CORPUSFREQ"] > 200 and self.dictionary[word]["CORPUSFREQ"] <= 1000:
                    scores.append(1)
                    continue
                if self.dictionary[word]["CORPUSFREQ"] > 1000 and self.dictionary[word]["CORPUSFREQ"] <= 2000:
                    scores.append(-1)
                    continue
                if self.dictionary[word]["CORPUSFREQ"] > 2000 and self.dictionary[word]["CORPUSFREQ"] <= 5000:
                    scores.append(-2)
                    continue
                if self.dictionary[word]["CORPUSFREQ"] > 5000:
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


def get_average_subordinations_per_section(db, start_location_1, start_location_2, end_location_1, end_location_2):
    '''
    Goes into Full AP MongoDB collection for text, so different LOCATION numbers, i.e., no more 1.4622, now it should be 1_4
    '''
    collection = db["Bridge_Latin_Text_Vergilius_Aeneis_VerAen_newAP_localdef_20230310"]

    # Fetch data from MongoDB
    cursor = collection.find({
        'LOCATION_1': {'$gte': start_location_1, '$lte': end_location_1},
        'LOCATION_2': {'$gte': start_location_2, '$lte': end_location_2}
    })

    # Convert cursor to DataFrame
    df = pd.DataFrame(list(cursor))

    # Ensure 'LOCATION_1' and 'LOCATION_2' are integers
    df[['LOCATION_1', 'LOCATION_2']] = df['LOCATION'].str.split('_', expand=True).astype(int)

    # Filter the DataFrame based on start and end locations
    start_condition = ((df['LOCATION_1'] >= start_location_1) & (df['LOCATION_2'] >= start_location_2))
    end_condition = ((df['LOCATION_1'] <= end_location_1) & (df['LOCATION_2'] <= end_location_2))
    df = df[start_condition & end_condition]

    # Count the total number of non-null entries in the 'SUBORDINATION_CODE' column for each section
    subordinations_per_section = df['SUBORDINATION_CODE'].notnull().groupby(df['SECTION']).sum()

    # Count the total number of sections
    num_sections = df['SECTION'].nunique()

    # Calculate the average subordinations
    if num_sections == 0:
        return 0  # Avoid division by zero
    average_subordinations = subordinations_per_section.sum() / num_sections

    return average_subordinations


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