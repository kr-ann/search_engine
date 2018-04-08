"""

This module is in charge of tokenization, i.e. it splits an input
string in sequences of tokens.

How a 'token' is understood is different in various methods.
The module contains classses for different kinds of 'tokens' and
class Tokenizer for performing tokenization.

"""

import unicodedata

class Basic_Token(object):   
    """

    A class for the first kind of token instances.
    A Token here is understood as a sequence of alphabethal symbols with a
    word, its start and end positions in a string, and its length.

    Has the following variables:
    word - our word (string of alphabethal symbols);
    start - the first position of our word in the string;
    end - the last position of the word in the string;
    length - the length of the word.

    """

    def __init__(self,word,start,end,length):
        """
        A method for making a class instance.
        """
        self.word = word
        self.start = start
        self.end = end
        self.length = length
    
    def __repr__(self):
        """
        A method to print a Token instance. Returns a string.
        """
        return "%s: [%s, %s, %s]" %(self.word, self.start, 
                                    self.end, self.length)

class Advanced_Token(object):
    """

    A class for the econd type of token instances.
    A Token here is understood as a sequence of symbols of the same
    kind with such sequence as a word, its start and end positions
    in a string, its length, and its kind.

    Has the following variables:
    word - our word (string of alphabethal symbols/digits/spaces);
    start - the first position of our word in the string;
    end - the last position of the word in the string;
    length - the length of the word;
    kind - the type of a token (alpha,space,digit,punct or other).

    """
    def __init__(self,word,start,end,length,kind):
        """
        A method for making a class instance.
        """
        self.word = word
        self.start = start
        self.end = end
        self.length = length
        self.kind = kind
    
    def __repr__(self):
        """
        A method to print a Token instance. Returns a string.
        """
        return "%s: [%s, %s, %s, %s]" %(self.word, self.start, 
                                    self.end, self.length, self.kind)


class Tokenizer(object):
    """
    This class is in charge of tokenization.
    
    Has the following methods:
    basic_tokenize - creates a list of Basic_Token instances.
    advanced_tokenize - cretes a list of Advanced_Token instances.
    iter_tokenize - a generator that yields a list of Advanced_Token instances.
    """
    
    def basic_tokenize(self,string):
        """
        Takes a string as an argument and creates a list of its Basic_Token instances.
        """
        current_word = ""
        start = 0
        end = 0
        length = 0
        
        our_list = []
        have_first_position = False   # indicates whether we already have the start position of a word
        first_char_after_word = False # shows that a word has ended - to include it in the list

        if not isinstance(string,str):
            raise ValueError("Tokenizer works only with strings. ")
        
        for i,char in enumerate(string):
            if char.isalpha():
                current_word = current_word + char
                if have_first_position == False:
                    start = i + 1 # to start from 1 and not from 0
                    have_first_position = True
                    
                first_char_after_word = True # now when the word ends we will append it in the list

                # if the symbol in last in the string we include the final word in the list
                if i == len(string) - 1:
                    end = i + 1 # because we start from 1, not from 0
                    length = end - start + 1
                    our_list.append(Basic_Token(current_word,start,end,length))
                continue
            
            if first_char_after_word: # when the previous word has ended
                end = i
                length = end -  start + 1
                our_list.append(Basic_Token(current_word,start,end,length))
                current_word = "" # clear this variable for the next word 
                first_char_after_word = False
                
            have_first_position = False # we are now ready for a new word

        return our_list


    def char_type(self,string):
        """
        Takes a string consisting of one character as an argument and
        returns its type (alpha,digit,space,punct or "other") as a string.
        """
        if len(string) > 1:
            raise ValueError("This method is only for characters. ")
        if string.isalpha():
            return "alpha"
        elif string.isdigit():
            return "digit"
        elif string.isspace():
            return "space"
        elif unicodedata.category(string).startswith('P'):
            return "punct"
        else:
            return "other"


    def advanced_tokenize(self,string):
        """
        Takes a string as an argument and creates a list of its Advanced_Token instances.
        """

        if not isinstance(string,str):
            raise ValueError("Tokenizer works only with strings. ")
        
        our_list = []
        
        # initialize this variable as a type of the first char in the string
        if not len(string) == 0:
            current_token_kind = Tokenizer().char_type(string[0])
        else:
            current_token_kind=""

        current_start = 1

        for i,char in enumerate(string):

            # if a type of the current token doesn't change when we go through
            # characters in the string - we do nothing
            if Tokenizer().char_type(char) == current_token_kind:
                pass

            # if a type of the current token has changed it means that the token
            # has ended and then we add it to the list
            else:
                our_list.append(Advanced_Token(string[current_start-1:i], current_start,
                                               i, i-current_start+1, current_token_kind))
                current_token_kind = Tokenizer().char_type(char)
                current_start = i+1
                
        # now we also have to append to the list the last token, because after it
        # a characters' type didn't change, so we didn't append it to the list yet -
        # but only if the string isn't empty
        if not len(string) == 0:
            our_list.append(Advanced_Token(string[current_start-1:len(string)], current_start,
                                           len(string), len(string)+1-current_start,
                                           Tokenizer().char_type(char)))

        return our_list

    
    def iter_tokenize(self,string):
        """
        Takes a string as an argument and yields its Advanced_Token instances.
        """
        if not isinstance(string,str):
            raise ValueError("Tokenizer works only with strings. ")
        
        # initialize this variable as a type of the first char in the string
        if not len(string) == 0:
            current_token_kind = Tokenizer().char_type(string[0])
        else:
            current_token_kind=""

        current_start = 1

        for i,char in enumerate(string):

            # if a type of the current token doesn't change when we go through
            # characters in the string - we do nothing
            if Tokenizer().char_type(char) == current_token_kind:
                pass

            # if a type of the current token has changed it means that the token
            # has ended and then we add it to the list    
            else:
                yield Advanced_Token(string[current_start-1:i], current_start,
                                     i, i-current_start+1, current_token_kind)
                current_token_kind = Tokenizer().char_type(char)
                current_start = i+1

        # now we also have to append to the list the last token, because after it
        # a characters' type didn't change, so we didn't append it to the list yet
        # but only if the string isn't empty
        if not len(string) == 0:
            yield Advanced_Token(string[current_start-1:len(string)], current_start,
                                 len(string), len(string)+1-current_start,
                                 Tokenizer().char_type(char))         
                
