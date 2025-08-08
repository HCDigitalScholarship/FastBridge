class Text(object):
    """A Text object for storing all the data and getting sections nicely"""

    def __init__(self, name : str, sections : dict, words : list, section_linkedlist : dict, subsections : int, language : str, local_def: bool = False, local_lem: bool = False):
        self.name = name
        self.sections = sections
        self.words =  words
        self.section_linkedlist = section_linkedlist
        self.subsections = subsections
        self.language = language
        self.local_def = local_def
        self.local_lem = local_lem


    def get_section(self, range_start, range_end):
        """
        Returns the tuple (start_index, end_index) for the words that fall between
        the given section identifiers. Assumes range_start and range_end are valid keys.
        """

        if range_start not in self.section_linkedlist:
            raise ValueError(f"Invalid start section: {range_start}")
        if range_end not in self.section_linkedlist and range_end != "end":
            raise ValueError(f"Invalid end section: {range_end}")

        # Get corresponding keys in self.sections
        # start is defined as index of end of previous section + 1 (index of previous section is the location last word of the previous section 0-indexed)
        start_idx = self.sections[self.section_linkedlist[range_start]] 
        if start_idx != 0: start_idx += 1 # don't add 1 if start_idx is 0

        if range_end == "end":
            end_idx = self.sections["end"] + 1
        else:
            end_idx = self.sections[range_end] + 1

        return start_idx, end_idx


    def get_words(self, user_start, user_end, stats=False, oracle=False):
        """
        Convienent wrapper method. Gets the correct sublist of TITLES, based on user's selection.
        """
        #text will usually be a text class that is our target text, for this early demo/figuring things out phase we will not use one, it is hardcoded to Ovid Met 1.
        #really: Text.text_list(), a method to return the text list if present and error other wise
        start, end = self.get_section(user_start, user_end)
        tmp = self.words

        if end == -1: end = len(tmp)
            
        if oracle: return [tmp[i][0] for i in range(start, end)] #returns only the wordforms, not the full tuple
        else: return [tmp[i] + (self.name,) if not stats else tmp[i] for i in range(start, end)] #adds the source text for select only


def next_section(section):
    """Handles the case where a section has letters in it. This should only be used in the cases where: input with one level and 2 level was expected and  with one level and 3 level was expected """
    working_section =  section.split(".") #so 1.1 = [1, 1],  2b.1 = [2b, 1], and 2b = [2b]
    try:
        target = str(int(working_section[0]) + 1)
    except ValueError: #invalid conversion
        target = f"{working_section[0][:-1]}{chr(ord(working_section[0][-1]) + 1)}"
    return target
