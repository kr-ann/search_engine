"""

This module is in charge of morphological analyzation (stemming).
Contains three stemmers of different complexity, and the function that decides
which of them to use: if the best one (BD_Stemmer) doesn't work (i.e. returns
nothing) - try the second (Flections_stemmer), then - the third (gen_simplest_stemmer).
The best stemmer can also return lemmas, not stems.

"""
import shelve

class Final_Stemmer(object):
    def __init__(self, stems_db, flections_db, path="C:\\Users\\boss\\Documents\\Python Scripts\\Search\\"):
        self.stems_db = shelve.open(path+stems_db)
        self.flections_db = shelve.open(path+flections_db)

    def __del__(self):
        self.stems_db.close()
        self.flections_db.close()
        print("Мы в функции удаления")
        
    def decide_and_return(self, word, lemmatisation=False):
        stemmer_obj = BD_Stemmer(self.stems_db, self.flections_db)
        best_result = list(stemmer_obj.gen_stemmer(word,lemmatisation))
        if best_result != []:
            print("Using the best stemmer")
            for stem in best_result:
                yield stem
        else: # the best stemmer failed to give any output
            flections = set(self.flections_db.keys())
            stemmer_obj = Flections_Stemmer(flections)
            second_result = list(stemmer_obj.gen_stemmer(word))
            if second_result != []:
                print("Using the second stemmer")
                for stem in second_result:
                    yield stem
            else: # the second stemmer also didn't manage
                print("Using the third stemmer")
                max_flexion_len = 3
                third_result = gen_simplest_stemmer(word, max_flexion_len)
                for stem in third_result: # the third stemmer always returns something
                    yield stem


def gen_simplest_stemmer(word, max_flexion_len):
    """
    The simplest stemmer that takes a word and a maximum flexion length
    as the input value and yields the word without the neach umber of
    last chracters (from 0 to the max_flexion_len).
    """
    if word == "" or type(word)!= str:
        raise ValueError("The input must be a non-empty string. ")
    
    if len(word) > max_flexion_len: # if the word is not too short
        for i in range(max_flexion_len+1):
            if i == 0:
                yield word
            else:
                yield word[:-i]
    else:
        yield word


class Flections_Stemmer(object):
    """
    Class for the stemmer that takes a list of flexions in the language.
    
    For the words that have more than 3 characters it tries to find a flection (i.e. n last characters)
    that would be present in the list of flections and return the remaining part of the word without
    the flection.
    
    """
    
    def __init__(self, flexions):
        self.flexions = set(flexions)
        self.max_flexion_len = len(max(flexions, key=len))

    def gen_stemmer(self, word):
        if word == "" or type(word)!= str:
            raise ValueError("The input must be a non-emty string. ")
        
        length = len(word)
        # we tried to set max_flection_length as a restriction for the length, but it equaled 8 and therefore was no good
        if length > 3: # if the word is not too short
            # если сделать range с нуля, то стеммер всегда будет что-то выдавать (слово в том же виде, что и на входе)
            # а нам это не нужно - для этого есть последний стеммер
            if length > self.max_flexion_len:
                upper_bound = self.max_flexion_len + 1 
            else:
                upper_bound = length
            for i in range(1, upper_bound):
                    flexion = word[length-i:]
                    if flexion in self.flexions:
                        yield word[:-i]
        else:
            yield word


class BD_Stemmer(object):
    """
    Class for the stemmer that takes two databases, with stems and flection, as an input.
    
    It tries to split a word into a stem and a flection so that both stem would be in the stems_db
    and flections - in the flections_db. Returns either the found stem or its lemma from the bd
    (if the lemmatisation parameter = True).
    """

    def __init__(self, opened_stems_db, opened_flections_db):
        self.stems_db = opened_stems_db
        self.flections_db = opened_flections_db

    def gen_stemmer(self, word, lemmatisation=False):
        for stem in self.stems_db:
            if word.startswith(stem):
                for flection in self.flections_db:
                    if word[word.index(stem)+len(stem):] == flection: # then word = stem + flection
                        intersection = self.flections_db[flection] & set(self.stems_db[stem].keys())
                        if intersection != set(): # if it's not empty - otherwise return nothing
                            if lemmatisation == False:
                                yield stem
                            else: # there can be different lemmas for one stem
                                for pair in intersection: # pairs like (template, variable_name)
                                    yield self.stems_db[stem][pair]
