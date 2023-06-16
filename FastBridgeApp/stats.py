import importlib
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px
from text import Text
from collections import defaultdict

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

def calculate_unique_words(text_instance: Text):
    '''
    Calculate the total amount of unique words
    '''
    #unique_words = len(set(word[0] for word in text_instance.words))
    unique_words = len(set([word_tuple[2] for word_tuple in text_instance.words]))
    print(f"Unique words: {unique_words}")

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


def calculate_average_word_length(words):
    return sum(len(word) for word in words) / len(words)


def get_avg_word_length(text_instance:Text):
    '''
    
    '''
    # Get words from each section
    sections = defaultdict(list)
    for word_tuple in text_instance.words:
        word = word_tuple[0]
        section = word_tuple[5]
        sections[section].append(word)

    # Calculate average word length and find hapax legomena per section
    for section, words in sections.items():
        average_word_length = calculate_average_word_length(words)
        print(f"Section {section}")
        print(f"  Average word length: {average_word_length}")





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
    '''
    start_index = text_object.sections[start_section]
    end_index = text_object.sections[end_section]
    text_slice = text_object.words[start_index:end_index]

    if start_section == 'start' and end_section == 'end':
        text_slice = text_object.words    

    df = pd.DataFrame(text_slice, columns=["Word", "Index", "Lemma", "Definition", "Notes", "Section", "Word Count"])
    df['Word Length'] = df['Word'].apply(len)
    avg_word_length = df.groupby('Section')['Word Length'].mean().reset_index()
    plt.figure(figsize=(10,5))
    sns.barplot(data=avg_word_length, x='Section', y='Word Length')
    plt.title('Average Word Length per Section')
    plt.xticks(rotation=90)
    plt.show()'''
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
    barplot = sns.barplot(data=avg_word_length, x='Section', y='Word Length')
    plt.title(f"Average Word Length per Section of {text_object.name}")
    
    # set x-tick labels with a step size
    for ind, label in enumerate(barplot.get_xticklabels()):
        if ind % step_size == 0:  # only show labels for every nth section
            label.set_visible(True)
        else:
            label.set_visible(False)

    plt.xticks(rotation=90)
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
    plt.figure(figsize=(10,5))
    sns.barplot(data=word_frequency[:30], x='Word', y='Frequency')
    plt.title(f"Word Frequency of {text_object.name}")
    plt.xticks(rotation=90)
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





#main()


# Using the get_text function to load the text instance
text_instance = get_text('vergil_aeneid_ap_selections', 'Latin').book  

# Call old functions
#calculate_total_words(text_instance)
#calculate_unique_words(text_instance)
#calculate_total_sections(text_instance)
#calculate_avg_words_per_section(text_instance)
#get_avg_word_length(text_instance)
#get_hapax_legomena(text_instance)




#Call new functions
print(get_number_of_words(text_instance, 'start', 'end'))
print(get_number_of_words(text_instance, '1.1', '1.422'))

print(get_vocabulary_size(text_instance, 'start', 'end'))
print(get_vocabulary_size(text_instance, '1.1', '1.422'))

#plot_avg_word_length(text_instance, 'start', 'end')
#plot_avg_word_length2(text_instance, '1.1', '6.899')
#plot_word_frequency(text_instance, 'start','end')

#print(get_hapax_legomena(text_instance, 'start', 'end'))
print(get_hapax_legomena(text_instance, '1.166', '1.422'))



