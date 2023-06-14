import importlib
from collections import defaultdict

def get_text(form_request : str, language : str):
    """
    Imports the text that was requested. This way, we only load the texts that the user is requesting each time.
    """
    return importlib.import_module(f'data.{language}.{form_request}') #point to the data folder

def calculate_total_words(text_instance):
    '''
    Calculate the total amount of words in the text given
    '''
    total_words = len(text_instance.words)
    print(f"Total number of words: {total_words}")

def calculate_unique_words(text_instance):
    '''
    Calculate the total amount of unique words
    '''
    #unique_words = len(set(word[0] for word in text_instance.words))
    unique_words = len(set([word_tuple[2] for word_tuple in text_instance.words]))
    print(f"Unique words: {unique_words}")

def calculate_total_sections(text_instance):
    '''
    Calculate the number of sections in the text
    '''
    total_sections = len(text_instance.sections)
    print(f"Total sections: {total_sections}")



def calculate_avg_words_per_section(text_instance):
    '''
    Calculate the avg number of words per section. Can also be words per sentence???
    '''
    total_words = len(text_instance.words)
    total_sections = len(text_instance.sections)
    avg_words_per_section = total_words / total_sections


    print(f"Average words per section: {avg_words_per_section:.2f}")


def calculate_average_word_length(words):
    return sum(len(word) for word in words) / len(words)

def find_hapax_legomena(words):
    word_frequencies = defaultdict(int)
    for word in words:
        word_frequencies[word] += 1
    return [word for word, freq in word_frequencies.items() if freq == 1]


def get_avg_word_length(text_instance):
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

def get_hapax_legomena(text_instance):
    '''
    Returns all of the words used once from each section, separated by section, it's just printing but can return in zip()
    '''
    # Get words from each section
    sections = defaultdict(list)
    for word_tuple in text_instance.words:
        word = word_tuple[0]
        section = word_tuple[5]
        sections[section].append(word)

    # find hapax legomena per section
    for section, words in sections.items():
        hapax_legomena = find_hapax_legomena(words)
        print(f"Section {section}")
        print(f"  Hapax legomena: {hapax_legomena}")


# Using the get_text function to load the text instance
text_instance = get_text('vergil_aeneid_ap_selections', 'Latin').book  # replace with your actual parameters

# Call each function
calculate_total_words(text_instance)
calculate_unique_words(text_instance)
calculate_total_sections(text_instance)
calculate_avg_words_per_section(text_instance)
#list_first_section_words(text_instance)


#get_avg_word_length(text_instance)
#get_hapax_legomena(text_instance)