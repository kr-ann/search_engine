"""

This module is in charge of creating an index, i.e. a dict consisting
of tokens and their positions.

How a 'position' is understood is different in various methods. Only
words and digits are considered tokens.
The module contains classes for different kinds of 'position' and
class Indexer for creating an index.

"""

import my_tokenizer_combined as t
import shelve
import functools

class Basic_Position(object):
    """

    A class for objects desccribing a token's position in a string.

    Has the following variables:
    start - an index of the first symbol of a token;
    end - an index of the last symbol of a token.

    """
    
    def __init__(self,start,end):
        self.start = start
        self.end = end

    def __eq__(self,obj2):
        return self.start==obj2.start and self.end==obj2.end

    def __repr__(self):
        return "[%s, %s]" %(self.start, self.end)

class Long_Position(Basic_Position):
    """

    A class for objects desccribing a token's position in a string.

    Has the following variables:
    start - an index of the first symbol of a token in a string;
    end - an index of the last symbol of a token in a string;
    string_numb - a number of the string in a file;
    file_name - a name of rhe file.

    """
    
    def __init__(self,start,end,string_numb,file_name):
        self.start = start
        self.end = end
        self.string_numb = string_numb
        self.file_name = file_name

    def __eq__(self,obj2):
        return self.start==obj2.start and self.end==obj2.end \
               and self.string_numb == obj2.string_numb \
               and self.file_name == obj2.file_name

    def __repr__(self):
        return "[start: %s, end: %s, string: %s, file: %s]" \
               %(self.start, self.end, self.string_numb, self.file_name)
    
@functools.total_ordering
class File_Position(Basic_Position):
    """

    A class for objects desccribing a token's position in a string.

    Has the following variables:
    start - an index of the first symbol of a token in a string;
    end - an index of the last symbol of a token in a string;
    string_numb - a number of the string in a file.

    """
        
    def __init__(self,start,end,string_numb):
        self.start = start
        self.end = end
        self.string_numb = string_numb

    def __eq__(self,obj2):
        return self.start==obj2.start and self.end==obj2.end \
               and self.string_numb == obj2.string_numb

    def __repr__(self):
        return "[start: %s, end: %s, string: %s]" \
               %(self.start, self.end, self.string_numb)

    def __lt__(self,obj2): # "less than" for File Positions
        if self.string_numb < obj2.string_numb:
            return True
        if self.string_numb > obj2.string_numb:
            return False
        if self.string_numb == obj2.string_numb:
            if self.start < obj2.start:
                return True
            if self.start > obj2.start:
                return False

class Indexer(object):
    """

    A class for creating an index.

    Contains three methods for creating an index from different inputs:
    one method creates an index from a string and two - from a file,
    they differ in structures of a result dict.
    Contains also a method to add an index from a file to a database.
    
    """

    def create_index_from_string(self,string):
        """
        Takes a string as an argument and creates a dictionary, which
        contains words or digits as keys and a list of their 'basic'
        positions in the string as values.
        """
        
        if not isinstance(string,str):
            raise ValueError("This indexer works only with strings. ")

        our_dict={}

        for obj in t.Tokenizer().iter_tokenize(string):
            
            # we include only words or digits in the final dict
            if obj.kind=="alpha" or obj.kind=="digit":
                
                # setdefault returns dict[key], adding a key with the default
                # value if the key is not in the dict yet
                l = our_dict.setdefault(obj.word,[])
                l.append(Basic_Position(obj.start,obj.end))

        return our_dict

    def create_long_index_from_file(self,path):
        """
        The method takes a name (a path) of a file as an input and
        creates a dict with a token as a key and a list of its 'long'
        positions as a value.
        """

        if not isinstance(path,str):
            raise ValueError("This method takes a string containing \
                              the name (a path) of a file as an input.")

        our_dict={}
        with open(path, encoding = "utf-8") as file:
            tokenizer = t.Tokenizer()
            for i,string in enumerate(file):
            
                # for each object in a generator
                for obj in tokenizer.iter_tokenize(string):
            
                    if obj.kind=="alpha" or obj.kind=="digit":
                        l = our_dict.setdefault(obj.word,[])
                        l.append(Long_Position(obj.start,obj.end, i+1, file.name))

        return our_dict

    def create_complex_index_from_file(self,path):
        """
        The method takes a name (a path) of a file as an input and
        creates a dict with a token as a key and a file and a list
        of its 'file' positions as a value.
        """

        if not isinstance(path,str):
            raise ValueError("This method takes a string containing \
                              the name (a path) of a file as an input.")

        our_dict = {}
        tokenizer = t.Tokenizer()
        with open(path, encoding = "utf-8") as file:
            for i,string in enumerate(file):
            
                # for each token out of a generator
                for token in tokenizer.iter_tokenize(string):

                    if token.kind=="alpha" or token.kind=="digit":

                        # internal - is a dict to store positions in one file
                        internal_dict = our_dict.setdefault(token.word,{})
                        positions_list = internal_dict.setdefault(file.name,[])
                        positions_list.append(File_Position(token.start,token.end,i+1))

        return our_dict

    def create_db_index(self, db_name, file_name):
        """
        The method is very much alike with the method 'create_complex_index_from_file',
        but it adds a computed index to a database rather than to a dict with a complex
        structure.
        """

        if (not isinstance(db_name,str)) or (not isinstance(file_name,str)):
            raise ValueError("This method takes two strings as an input: \
                              names (paths) of a db and a file. ")

        with shelve.open(db_name,writeback=True) as db:
        
            tokenizer = t.Tokenizer()
            # the same as in the method create_complex_index_from_file
            with open(file_name, encoding = "utf-8") as file:
                for i,string in enumerate(file):
                
                    # for each token out of a generator
                    for token in tokenizer.iter_tokenize(string):

                        if token.kind=="alpha" or token.kind=="digit":

                            # internal - is a dict to store positions in one file
                            internal_dict = db.setdefault(token.word,{})
                            positions_list = internal_dict.setdefault(file.name,[])
                            positions_list.append(File_Position(token.start,token.end,i+1))

        
    
        
