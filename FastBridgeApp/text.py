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
        Converts the human section citation of 1-3 sections to the keys of the section dictionary, and retrives the indices for self.words that the sections correspond to.

        """
        print(range_start, "start")
        print(range_end, "end")
        if range_start == "start":
            internal_range_start =  range_start
        elif range_start.count(".") == 0 and self.subsections == 1:
        #for things with one level and 1 level is expected
            internal_range_start =  range_start
        elif range_start.count(".") == 0 and self.subsections == 2:
        #for things with one level and 2 level was expected
            internal_range_start = range_start + ".1"
        elif range_start.count(".") == 0 and self.subsections == 3:
            #for things with one level and 3 level was expected
                internal_range_start = range_start + ".1.1"
        elif range_start.count(".") == 1 and self.subsections == 2:
            print("start of depth 2, as expected")
            #for things with two levels, and two were given
            internal_range_start = range_start
            print(internal_range_start)
        elif range_start.count(".") == 1 and self.subsections == 3:
            #for things with three levels, and two were given
            internal_range_start = range_start + ".1"
        elif range_start.count(".") == 2 and self.subsections == 3:
            internal_range_start = range_start
        if range_end == "end" or range_end == "start":
            internal_range_end = range_end
        elif range_end.count(".") == 0 and self.subsections == 1:
            #for input with one level and 1 level is expected
                internal_range_end = range_end
        elif range_end.count(".") == 0 and self.subsections == 2:
            #for input with one level and 2 level was expected
            try:
                internal_range_end = self.section_linkedlist[next_section(range_end) + ".1"]
                #this should make a search for  1.1 - 1 become a search for 1.1 - 2.1(previous section). If the section has a letter (ie, 2b), this will convert it to 2c. If 2c does not exist, it will fail and go below
            except Exception as e:
                to_increment = range_end[:-1] #remove the letter
                self.section_linkedlist[next_section(to_increment) + ".1"]

        elif range_end.count(".") == 0 and self.subsections == 3:
            #for things with one level and 3 level was expected
            try:
                internal_range_end = self.section_linkedlist[next_section(range_end) + ".1.1"]
            except Exception as e:
                to_increment = range_end[:-1] #remove the letter
                self.section_linkedlist[next_section(to_increment) + ".1.1"]

        elif range_end.count(".") == 1 and self.subsections == 2:
            print("end of depth 2, as expected")
                #for things with two levels, and two were given
            internal_range_end =  range_end
            print(internal_range_end)
        elif range_end.count(".") == 1 and self.subsections == 3:
            #for things with three levels, and two were given
            range_end = range_end.split(".")
            try:
                internal_range_end = self.section_linkedlist[".".join(range_end[0], next_section(range_end[1]), ".1")]
            except Exception as e:
                internal_range_end = self.section_linkedlist[".".join(range_end[0], next_section(range_end[1][:-1]), ".1")]
        elif range_end.count(".") == 2 and self.subsections == 3:
            internal_range_end = range_end
        #start ends up being the end of the previous section + 1
        #print(internal_range_start, " starting place")
        #print(internal_range_end, " ending place")

        #print(self.sections[self.section_linkedlist[internal_range_start]] +1)
        #print(self.sections[internal_range_end] +1)
        #print((self.sections[self.section_linkedlist[internal_range_start]] + 1, (self.sections[internal_range_end]+1)))
        print(self.sections[internal_range_end]) #should be the end list index
        print(self.section_linkedlist[internal_range_start])
        return (self.sections[self.section_linkedlist[internal_range_start]] + 1, (self.sections[internal_range_end]+1))



    def get_words(self, user_start, user_end):
        """
        Convienent wrapper method. Gets the correct sublist of TITLES, based on user's selection.
        """
        #text will usually be a text class that is our target text, for this early demo/figuring things out phase we will not use one, it is hardcoded to Ovid Met 1.
        #really: Text.text_list(), a method to return the text list if present and error other wise
        start, end = self.get_section(user_start, user_end)
        #print(start, end)
        tmp = self.words

        if end == -1:
            end = len(tmp)
        wordlist = [tmp[i] + (self.name,) for i in range(start, end)] #adds the source text
        return wordlist


def next_section(section):
    """Handles the case where a section has letters in it. This should only be used in the cases where: input with one level and 2 level was expected and  with one level and 3 level was expected """
    working_section =  section.split(".") #so 1.1 = [1, 1],  2b.1 = [2b, 1], and 2b = [2b]
    try:
        target = str(int(working_section[0]) + 1)
    except ValueError: #invalid conversion
        target = f"{working_section[0][:-1]}{chr(ord(working_section[0][-1]) + 1)}"
    return target
