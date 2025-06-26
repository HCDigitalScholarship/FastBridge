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
        Normalizes the range_start and range_end section identifiers to match the expected
        self.subsections format, then returns a tuple of (start_index, end_index) for self.words.
        """

        def normalize_section(section, is_start):
            if section in ("start", "end"):
                return section

            num_dots = section.count(".")
            if self.subsections == 0 or self.subsections == 1:
                # Accept anything as-is for flat structures
                return section

            elif self.subsections == 2:
                if num_dots == 0:
                    return section + ".1"
                elif num_dots == 1:
                    return section
                elif num_dots > 1:
                    raise ValueError(f"Too many subsections in '{section}' for expected level 2.")

            elif self.subsections == 3:
                if num_dots == 0:
                    return section + ".1.1"
                elif num_dots == 1:
                    return section + ".1"
                elif num_dots == 2:
                    return section
                else:
                    raise ValueError(f"Too many subsections in '{section}' for expected level 3.")

            raise ValueError(f"Unsupported subsection level: {self.subsections}")

        def resolve_end(section):
            if section in ("start", "end"):
                return section

            normalized = normalize_section(section, is_start=False)

            if normalized in self.section_linkedlist:
                return normalized

            try:
                # Try next section if normalized key is missing
                base = section.rstrip("abcdefghijklmnopqrstuvwxyz")  # remove trailing letter if any
                next_sec = next_section(base)

                if self.subsections == 1:
                    return next_sec
                elif self.subsections == 2:
                    return next_sec + ".1"
                elif self.subsections == 3:
                    return next_sec + ".1.1"
            except Exception as e:
                raise KeyError(f"Could not resolve section end '{section}' due to: {e}")

        # Normalize range_start
        try:
            internal_range_start = normalize_section(range_start, is_start=True)
        except Exception as e:
            raise ValueError(f"Failed to normalize start section '{range_start}': {e}")

        # Normalize and resolve range_end
        try:
            internal_range_end = resolve_end(range_end)
        except Exception as e:
            raise ValueError(f"Failed to normalize end section '{range_end}': {e}")


        # Convert to indices
        try:
            start_idx = self.sections[self.section_linkedlist[internal_range_start]] + 1
            if internal_range_end in ("start", "end"):
                end_idx = self.sections[internal_range_end] + 1  # Assume end is mapped
            else:
                end_idx = self.sections[internal_range_end] + 1
        except KeyError as e:
            raise KeyError(f"Missing key in section_linkedlist or sections: {e}")

        return start_idx, end_idx




    def get_words(self, user_start, user_end):
        """
        Convienent wrapper method. Gets the correct sublist of TITLES, based on user's selection.
        """
        #text will usually be a text class that is our target text, for this early demo/figuring things out phase we will not use one, it is hardcoded to Ovid Met 1.
        #really: Text.text_list(), a method to return the text list if present and error other wise
        start, end = self.get_section(user_start, user_end)
        tmp = self.words

        if end == -1:
            end = len(tmp)
        wordlist = [tmp[i] + (self.name,) for i in range(start, end)] #adds the source text
        return wordlist
    
    def get_slice(self, start_section, end_section):
        if start_section == 'start' and end_section == 'end': return self.words
        
        start_index = self.sections[start_section]
        end_index = self.sections[end_section]
        text_slice = self.words[start_index:end_index]


        return text_slice


def next_section(section):
    """Handles the case where a section has letters in it. This should only be used in the cases where: input with one level and 2 level was expected and  with one level and 3 level was expected """
    working_section =  section.split(".") #so 1.1 = [1, 1],  2b.1 = [2b, 1], and 2b = [2b]
    try:
        target = str(int(working_section[0]) + 1)
    except ValueError: #invalid conversion
        target = f"{working_section[0][:-1]}{chr(ord(working_section[0][-1]) + 1)}"
    return target
