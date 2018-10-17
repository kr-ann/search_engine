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
    
    def __lt__(self,obj2):
        if self.start < obj2.start:
            return True
        if self.start > obj2.start:
            return False
        if self.start == obj2.start:
            # there shouldn't be any cases where both start and end are equal, but just in case
            if self.end <= obj2.end: 
                return True
            if self.end > obj2.end:
                return False
            
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

    def abstract_iterator(self,list_of_lists):
        """
        Simultaneous sorting.
        Takes an iterable of iterables and yields elements in the ascending order.
        """
        # list_of_iter_lists contains iterators for each list in list_of_lists
        list_of_iter_lists = []
        try:
            for sorted_list in list_of_lists:
                list_of_iter_lists.append(iter(sorted_list))
        except TypeError:
            # is raise if either outer "list" or inner "lists" are not iterable
            raise TypeError("The input parapeter must be iterable.")        

        first_elements = []
        for iter_list in list_of_iter_lists:
            first_elements.append(next(iter_list)) # first elements in each iter_list

        while len(first_elements)>0: # if len = 0 then all ietrators have ended
            min_el = min(first_elements)

            # proceed to the next element in the list from which we took the min_el
            min_ind = first_elements.index(min_el)
            try:
                first_elements[min_ind] = next(list_of_iter_lists[min_ind])
            except StopIteration:
                first_elements.pop(min_ind)
                list_of_iter_lists.pop(min_ind)
            yield min_el
    
    def the_simplest(self,token):
        """
        A method that returns a dict with file names as keys and positions of token
        within these files as values. 
        """
        if not isinstance(token,str):
            raise ValueError("The argument should be a string containing a token.")

        if token not in self.db:
            return {}
        
        return self.db[token]
        
        
    def the_second_simplest(self,query,doc_limit,doc_offset): #### NEW ####
        """
        A method that returns a dict with GENERATOR of positions of tokens from the
        query in files. 

        It takes a string 'query' as an input, tokenizes it, and returns a dict with
        names of files (that contain all tokens of the input) as keys and GENERATORS from
        lists of positions in those files as values.
        Its arguments also include 'doc_limit' and 'doc_offset', which indicate what
        part of documents will be shown on the final page via our server.
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
                

        list_from_set = list(set_for_all)
        list_from_set.sort()
        # now we take only part of list_from_set
        new_list = list_from_set[doc_offset:doc_offset+doc_limit]

        ### NEW ###
        # create dict with file names as keys and list of lists as values, where
        # each inner list contains positions in this file for one word from a query
        for file in new_list:
            tokens = t.iter_tokenize(query)
            list_of_lists = []
            for token in tokens:
                current_list = []
                if token.kind == "alpha" or token.kind == "digit":
                    current_list = self.the_simplest(token.word)[file]
                    list_of_lists.append(current_list)
            # for abstract_iterator to deal with context windows we defined __lt__ for them
            dict_for_all[file]=self.abstract_iterator(list_of_lists)
            
            # here we delete equal positions, otherwise we get "князькнязь..."
            dict_for_all[file] = self.gen_delete_equal(dict_for_all[file])
            
        return dict_for_all

    ### NEW ###
    def gen_delete_equal(self,gen_pos):
        """
        To delete equal positions from generator of positions.
        """
        
        dont_go_further = False # boolean - to yield only one position if it's the only in the gen 
        try:
            first = next(gen_pos) # in case generator is empty
        except StopIteration:
            raise ValueError("Generator of positions in the method gen_delete_equal is empty")
        try:
            second = next(gen_pos) # in case generator contains only one element
        except StopIteration:
            yield first
            dont_go_further = True
            
        while dont_go_further == False:
            if first==second:
                first=second
                try:
                    second=next(gen_pos)
                except StopIteration:
                    yield first
                    break
            else:
                yield first
                first = second
                try:
                    second=next(gen_pos)
                except StopIteration:
                    yield first
                    break
            
            
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
        Returns a Context_Window instance for a word, given its position in a file.

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


    def gen_context_windows(self,gen_positions_dict,file_name,length): ### NEW ###
        """
        This function returns context windows (it's a generator).
        
        It gets as input teh following parameters:
        gen_positions_dict - a dict with file names as keys and generators of positions
                             as values;
        file_name - name of the file for which we will yield positions;
        length - the length of context windows.
        """
        with open(file_name, encoding = 'utf-8') as f:
            file_enum = enumerate(f) # will go through strings in a file

            # initialization of file_string_numb and position
            file_string_numb, current_string = next(file_enum)
            position = next(gen_positions_dict[file_name])

            # simultaneously go throug lines in the file and through sorted positions
            while True:
                if file_string_numb + 1 < position.string_numb:
                    try:
                        file_string_numb, current_string = next(file_enum)
                    except StopIteration:
                        break
                if file_string_numb + 1 == position.string_numb:
                    window = self.get_window(position, current_string, length)
                    try:
                        position = next(gen_positions_dict[file_name])
                        yield window
                    except StopIteration:
                        yield window
                        break

    
    def get_context_for_words(self,query,length,doc_limit,doc_offset): ### NEW ###
        """
        The method that returns contexts for all words from the query.
        
        It takes a query and a length of desired context and returns a dict with file
        names as keys and GENERATORS FROM lists of Context_Window instances for words
        and digits in the query. Context windows are joined into one if they intersect.
        Its arguments also include 'doc_limit' and 'doc_offset', which indicate what
        part of documents will be shown on the final page via our server.
        """
        if not isinstance(query,str):
            raise ValueError("The first argument should be a string.")
        if not isinstance(length,int):
            raise ValueError("The second argument should be an integer number.")

        # with the help of the_second_simplest we get a sorted dict with file names
        # as keys and GENERATOR of positions of words from the query as values
        gen_positions_dict = self.the_second_simplest(query,doc_limit,doc_offset)

        gen_windows_dict = {}
        for file in gen_positions_dict: # dict with generators of context windows for each file
            gen_windows_dict[file]=self.gen_context_windows(gen_positions_dict,file,length)

        # now we join overlapping windows in the gen_windows_dict
        return self.join_windows(gen_windows_dict) # returns a generator
    
    def join_windows(self, gen_windows_dict):
        """
        It joins overlapping windows in the gen_windows_list that is given as an argument.
        gen_windows_dict contains file names as keys and generarors of Context_Window instances
        as values.
        """
        for key in gen_windows_dict:
            gen_windows_dict[key] = self.gen_for_joining(gen_windows_dict[key])
        return gen_windows_dict
    
    def gen_for_joining(self,gen_windows): ### NEW ###
        """
        Generator for joining windows - gets a generator of windows as an input and
        yields joined ones (if they intersect).
        """
        # all windows.file_pos_list in gen_windows intially contain only one position
        dont_go_further = False # to yield only one position if it's the only one in the gen
        try:
            first = next(gen_windows) # in case generator is empty
        except StopIteration:
            raise ValueError("Generator of windows in the method gen_for_joining is empty")
        try:
            second = next(gen_windows) # in case generator contains only one element
        except StopIteration:
            yield first
            dont_go_further = True
            
        while dont_go_further == False:
            if first.intersects(second):
                file_pos_list = first.file_pos_list + second.file_pos_list
                # contexts are the same string
                first = Context_Window(file_pos_list,first.start,second.end,first.context)
                try:
                    second = next(gen_windows)
                except StopIteration:
                    yield first
                    break
            else:
                yield first
                first = second
                try:
                    second = next(gen_windows)
                except StopIteration:
                    yield first
                    break
                

    def end_of_sentence(self, string):
        """
        Rules for establishing that we've run against an end of sentence.
        """
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
    

    def make_windows_sentences(self,gen_windows_dict,lim_off_list):
        """
        The method that expands boundaries of Context_windows to match boundaries
        of sentences.

        Takes as an argument a dict with file names as keys and context windows
        as values. Its arguments also include 'lim_off_list', which contains
        pairs (limit,offset) that show what part of citations will be shown on
        the final page via server - for each corresponding document.
        """
        for key in gen_windows_dict:
            gen_windows_dict[key]=self.gen_making_windows_sentences(gen_windows_dict[key])

        # now we join overlapping windows in the windows_dict
        # 'joined' is a dict, and values are generators
        joined = self.join_windows(gen_windows_dict)
        
        # now we have to return only part of "joined", taking lim_off_list into account
        result_dict = {}
        for i,key in enumerate(joined):
            result_list = []
            counter = 0
            while counter < lim_off_list[i][1]: # offset for the corresponding document
                try:
                    window = next(joined[key])
                    counter += 1
                except StopIteration:
                    counter=lim_off_list[i][1] # чтобы выйти из внутреннего цикла
                    
            counter = 0
            while counter < lim_off_list[i][0]: # limit for the corresponding document
                try:
                    result_list.append(next(joined[key]))
                    counter += 1
                except StopIteration:
                    # the number of elements is less then the limit
                    counter=lim_off_list[i][0] # чтобы выйти из внутреннего цикла
                    
            result_dict[key] = result_list
                
        return result_dict
            
    def gen_making_windows_sentences(self,gen_windows): ### NEW ###
        """
        Generator for making windows sentences (making windows bigger so as they
        contain one or several sentences). Gets generator of windows as an input.
        """
        for window in gen_windows:
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
                    if self.end_of_sentence(left_part_of_context[i:i+4][::-1]): # inverted string
                        window.start = window.start - i 
                        break
                    
                except IndexError:
                    window.start = 1
                    break
            yield window

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
