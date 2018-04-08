"""

This module is in charge of performing search given a database witn tokens and their
positions. And also of representing the results using context windows.

"""

import shelve
import my_tokenizer_combined
import my_indexer_combined

class Context_Window(object):
    """

    A class for our context windows.

    Has the followig variables:
    file_pos_list - a list of File_Position instances that contain
                    a position of an initial word in a file;
    start - a start position of a context in a string,
    end - an end position of a context in a string,
    context - the whole string from a file containig the context.
    
    """

    def __init__(self,file_pos_list,start,end,context):
        self.file_pos_list = file_pos_list
        self.start = start
        self.end = end
        self.context = context

    def __repr__(self):
        # A Context_Window instance has the whole string from a file as an argument,
        # but it prints out only the part of it: from self.start to self.end
        return "КОНТЕКСТ:[%s] ПОЗИЦИИ: [%s - %s]" %(self.context[self.start-1:self.end],
                                                    self.start, self.end)

    def __eq__(self,obj2):
        return self.start==obj2.start and self.end==obj2.end\
               and self.file_pos_list==obj2.file_pos_list \
               and self.context==obj2.context # maybe it's not necessary
    
    def __hash__(self):
        return hash((self.start, self.end, self.context))

    def intersects(self,window2):
        """
        Checks whether two windows intersect.
        We will need this method for joining windows.
        """
        return self.file_pos_list[0].string_numb == window2.file_pos_list[0].string_numb\
               and self.end >= window2.start
        
class Engine(object):
    """

    A class that performs search.

    Its instances have one variable: path - a path to (a name of) a previously made
    database witn tokens and their positions.
    
    """

    def __init__(self,path):
        self.path = path
        self.db = shelve.open(self.path)

    def __del__(self):
        self.db.close()
    
    def the_simplest(self,token):
        """
        A method that returns a dict with file names as keys and positions of tokens
        within these files as values. 
        """

        if not isinstance(token,str):
            raise ValueError("The argument should be a string containing a token.")

        if token not in self.db:
            return {}
        
        return self.db[token]
            
        
    def the_second_simplest(self,query):
        """
        A method that returns a dict with positions of tokens from the query in files. 

        It takes a string as an input, tokenizes it, and returns a dict with names
        of files (that contain all tokens of the input) as keys and lists of their
        positions in those files as values.
        """
        
        if not isinstance(query,str):
            raise ValueError("An argument should be a string.")

        dict_for_all = {}
        t = my_tokenizer_combined.Tokenizer()
        tokens = t.iter_tokenize(query.strip()) # delete first and last spaces

        
        # intersetion of keys - files, containing all tokens of the input.
        # here we collect them and write to the variable set_for_all
        for i,token in enumerate(tokens):
            if token.kind == "alpha" or token.kind == "digit":
                if i == 0:
                    set_for_all = set(self.the_simplest(token.word))

                set_for_all &= set(self.the_simplest(token.word))


        # here we create the final dict
        tokens = t.iter_tokenize(query)
        for token in tokens:
            if token.kind == "alpha" or token.kind == "digit":
                for file in set_for_all:
                    conjunction = dict_for_all.setdefault(file,[])
                    # the_simplest method returns a dict with file names as keys
                    conjunction += self.the_simplest(token.word)[file]

        # here for each key we sort its values' list (i.e. positions' list)
        for key in dict_for_all:
            dict_for_all[key].sort()

        ### NEW ###
        
        # here we go through all positions (i.e. values for each key that are file names)
        # and delete those which are the same
        for key in dict_for_all:
            new_positions = dict_for_all[key] # they are sorted
            i = 0
            while i < len(new_positions)-1:
                if new_positions[i] == new_positions[i+1]:
                    new_positions.pop(i)
                else:
                    i+=1
            dict_for_all[key] = new_positions

        return dict_for_all

    def get_word(self,file,file_pos):
        """
        The method returns a word given its position in a file.

        Takes the following arguments:
        file - the file name
        file_pos - position of a word in a file
        """
        
        if not isinstance(file,str):
            raise ValueError("The first argument should be a string with file name.")
        if not isinstance(file_pos,my_indexer_combined.File_Position):
            raise ValueError("The second argument should be a File_Position instance.")
        
        with open(file, encoding = "utf-8") as file:
            for i,string in enumerate(file):
                # all these +-1 is because we count things from 1 and not from 0
                if file_pos.string_numb == i+1: 
                    result = string[file_pos.start-1:file_pos.end]
                    break
        return result

    def get_context(self,file,file_pos,length):
        """
        Returns a context of a word (i.e. "length" words before & after), given its 
        position in a file.

        Takes the following arguments:
        file - the file name
        file_pos - a position of a word in a file
        length - the length of a context window
        """

        if not isinstance(file,str):
            raise ValueError("The first argument should be a string with file name.")
        if not isinstance(file_pos,my_indexer_combined.File_Position):
            raise ValueError("The second argument should be a File_Position instance.")   
        if not isinstance(length,int):
            raise ValueError("The third argument should be an integer number.")


        tokenizer = my_tokenizer_combined.Tokenizer()

        with open(file, encoding="utf-8") as f:
            # tokenize a sub-string to the right and an inverted sub-string to the left
            for i,string in enumerate(f):
                # we need to count lines to check smth later
                if file_pos.string_numb == i+1:
                    right_string = string

        # string[start:end:-1] returns an inverted string
        j=0 # j - is just a counter
        start = 1 # if the 'lenght' of a context will go out of the string's range
        if file_pos.start != 1: # otherwise start = 1 and we don't need to alter it
            for token in tokenizer.iter_tokenize(right_string[file_pos.start-2::-1]):
                if j < length:
                    if token.kind == "alpha" or token.kind == "digit":
                        j += 1
                    continue
                
                # cause we go through an inverted string
                start = file_pos.start - token.end + 1
                break

        n=0
        # in case the 'lenght' of a context goes out of the string's range.
        end = len(right_string) - 1 # cause the last symbol is '\n' - we don't need it
        for token in tokenizer.iter_tokenize(right_string[file_pos.end:]):
            if n < length:
                if token.kind == "alpha" or token.kind == "digit":
                    n += 1
                continue

            # cause 'token.end' is got from a substring
            end = file_pos.end + token.end - 1
            break

        window = Context_Window([file_pos],start,end,right_string[:-1])
            
        return window

    def join_windows(self, windows_dict):
        """
        It joins overlapping windows in the windows_list that is given as an argument.
        """
        # in windows_list all windows.file_pos_list intially contain only one position
        for key in windows_dict:
            i=0
            windows_list = windows_dict[key]
            # cause we always compare list[i] with list[i+1]
            while i < len(windows_list)-1:
                if windows_list[i].intersects(windows_list[i+1]):
                    # don't create a new window, but rather change arguments of
                    # windows_list[i] and then delete windows_list[i+1]
                    windows_list[i].file_pos_list += windows_list[i+1].file_pos_list
                    # start and context are the same
                    windows_list[i].end = windows_list[i+1].end
                    
                    windows_list.pop(i+1)
               
                    # at the next step we should compare, again, windows_list[i] with
                    # windows_list[i+1] so we don't increase "i"
                    continue
                
                else:
                    i+=1
        return windows_dict


    def get_window(self, file_pos, right_string, length):
        """
        Returns a Context_Window instance, given a position of a word in a file,
        the corresponding string from the file and the length of the window.
        """
        # this part of code is from get_context method
        tokenizer = my_tokenizer_combined.Tokenizer()
        # string[start:end:-1] returns an inverted string
        j=0 # j - is just a counter
        start = 1 # if the 'lenght' of a context will go out of the string's range
        if file_pos.start != 1: # otherwise start = 1 and we don't need to alter it
            for token in tokenizer.iter_tokenize(right_string[file_pos.start-2::-1]):
                if j < length:
                    if token.kind == "alpha" or token.kind == "digit":
                        j += 1
                    continue
                
                # cause we go through an inverted string
                start = file_pos.start - token.end + 1
                break

        n=0
        # in case the 'lenght' of a context goes out of the string's range.
        end = len(right_string) - 1 # cause the last symbol is '\r' - we don't need it
        for token in tokenizer.iter_tokenize(right_string[file_pos.end:]):
            if n < length:
                if token.kind == "alpha" or token.kind == "digit":
                    n += 1
                continue

            # cause 'token.end' is got from a substring
            end = file_pos.end + token.end - 1
            break
        # [:-1] - not to include the final '\r'
        return Context_Window([file_pos],start,end,right_string[:-1])
        

    def get_context_for_words(self,query,length):
        """
        The method that returns contexts for all words from the query.
        
        It takes a query and a length of desired context and returns a dict with file
        names as keys and lists of Context_Window instances for words and digits in
        the query. Context windows are joined into one if they intersect.
        """
        
        if not isinstance(query,str):
            raise ValueError("The first argument should be a string.")
        if not isinstance(length,int):
            raise ValueError("The second argument should be an integer number.")

        # with the help of the_second_simplest we get a sorted dict with file names
        # as keys and positions of words from the query as values
        positions_dict = self.the_second_simplest(query)

        # dict with file names as keys and window_lists as values
        windows_dict = {}

        # here we go through strings and token positions within a file simultaneously
        for file in positions_dict:
            f = open(file, encoding = 'utf-8')
            file_enum = enumerate(f) # will go through strings in a file
                
            windows_list = []
            pos_iter = iter(positions_dict[file]) # through File_Position instances

            # initialization of file_string_numb & current_pos
            file_string_numb, current_string = next(file_enum)
            current_pos = next(pos_iter)

            while True:
                if file_string_numb + 1 < current_pos.string_numb:
                    try:
                        file_string_numb, current_string = next(file_enum)
                    except StopIteration:
                        break
                    
                if file_string_numb + 1 == current_pos.string_numb:
                    window = self.get_window(current_pos, current_string, length)
                    windows_list.append(window)
                    
                    try:
                        current_pos = next(pos_iter)
                    except StopIteration:
                        break
  
            windows_dict[file] = windows_list
            f.close()

        # now we join overlapping windows in the windows_dict
        return self.join_windows(windows_dict)

    def end_of_sentence(self, string):
        c0 = string[0]
        c1 = string[1]
        c2 = string[2]
        c3 = string[3]
        if (((c0 == '.' or c0 == '!' or c0 == '?') and (c1 == ' ') \
           and (
               (c2.isupper()) or ( (c2 == "'" or c2 == '"' or \
                                    c2 == "«" or c2 == "(" or\
                                    c2 == "„" or c2 == "“") \
                                   and (c3.isupper()) 
                                  )))
               or (
                   (c0 == '.' or c0 == '!' or c0 == '?') and (c1 == ')')\
                   and (c2 == " ")
                   )):
            return True
        
        else:
            return False
    

    def make_windows_sentences(self, windows_dict):
        """
        The method that expands boundaries of Context_windows to match boundaries
        of sentences.

        Takes as an argument a dict with file names as keys and context windows
        as values.
        """
        

        for key in windows_dict:
            for window in windows_dict[key]:
                # move to the right
                right_part_of_context = window.context[window.end-1:]
                
                for i,char in enumerate(right_part_of_context):
                    try:
                        if self.end_of_sentence(right_part_of_context[i:i+4]):                            
                            window.end = window.end + i
                            break

                    except IndexError:
                        window.end = len(window.context)
                        break
                
                # move to the left
                left_part_of_context = window.context[window.start::-1]
                for i, char in enumerate(left_part_of_context):
                    try:
                        if self.end_of_sentence(left_part_of_context[i:i+4][::-1]):
                            window.start = window.start - i 
                            break
                        
                    except IndexError:
                        window.start = 1
                        break
                
        # now we join overlapping windows in the windows_dict
        return self.join_windows(windows_dict)

    def make_dict_with_citations(self,dict_with_windows):
        """
        The function returns a dict, in which keys are file names and values are citations,
        extracted from Context Windows, with the query words in bold (i.e. in the <b></b> tag).
        """
    
        final_dict = {}
        for key in dict_with_windows:
            citations_list = []
            for window in dict_with_windows[key]:
                for i,pos in enumerate(window.file_pos_list):
                    if i == 0:
                        # the part from the beginning to the end of the first query word
                        citation = window.context[window.start-1:pos.start-1]+"<b>"\
                              +window.context[pos.start-1:pos.end]+"</b>"
                    else:
                        # from where we've stopped till the end of the next query word
                        citation += window.context[window.file_pos_list[i-1].end:pos.start-1]\
                                +"<b>"+window.context[pos.start-1:pos.end]+"</b>"
                    if i == len(window.file_pos_list)-1:
                        # from where we've stopped till the end
                        citation += window.context[pos.end:window.end]
                    
                citations_list.append(citation.strip())
                
            final_dict[key] = citations_list
        return final_dict
                

        
