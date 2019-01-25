"""
A module for creating two databases.
One contains stems as keys and inner dicts as values. In the inner dicts keys are
pairs (template, variable_name), and values are lemmas.
The other db has flections as keys and pairs (template, variable_name) as values.
Variable names are mostly either "основа" or "основа1", but there also can be
ones like "основа2" etc.
"""

import mwclient as mw
import shelve
import codecs
import threading


class Threads_for_stems_dict(threading.Thread):
    def __init__(self, online_dict, words_list, set_with_redirections):
        threading.Thread.__init__(self)
        self.online_dict = online_dict
        self.words_list = words_list
        self.set_with_redirections = set_with_redirections

        
    def run(self):
        print(threading.currentThread().getName() + '\n')
        site = mw.Site('ru.wiktionary.org')
        for word in self.words_list:
            word = word.strip()
            if not word:
                continue
            triples_set = stems(site, word, self.set_with_redirections)
            # if ther're no templates for a word, triples_set is empty, and
            # nothing happens (we just proceed to the next word)
            for triple in triples_set: # triples_set = (stem, template, variable_name)
                if triple[0] and triple[1] and triple[2]:  # check that all triple's elememts exist 
                    l = self.online_dict.setdefault(triple[0], {})
                    l[(triple[1], triple[2])] = word.lower() # "word" is a lemma
                else:
                    print("SOMETHING IS ABSENT IN THE TRIPLE", triple)
                    continue
                
        return


class Threads_for_flections_dict(threading.Thread):
    def __init__(self, online_dict, templates_list):
        threading.Thread.__init__(self)
        self.online_dict = online_dict
        self.templates_list = templates_list

        
    def run(self):
        print(threading.currentThread().getName() + '\n')
        site = mw.Site('ru.wiktionary.org')
        for template in self.templates_list:
            template = template.strip()
            if not template:
                continue
            flections_dict = flections(site, template[7:]) # remove the "Шаблон:" part
            for variable_name in flections_dict:
                for flection in flections_dict[variable_name]:
                    l = self.online_dict.setdefault(flection, set())
                    l.add((template, variable_name))
                    
        return
    
 
def templates(site, word):
    """
    Given a word as a string, returns a list of templates' names
    that are used on the word's page.
    """
    page = site.Pages[word]
    templates_list = []
    for obj in page.templates():
        if ("Шаблон:сущ ru " in obj.name and "Шаблон:сущ ru 2" not in obj.name) or "Шаблон:Фам ru" in obj.name:
            # Шаблон:сущ ru 2 does not have stems, it's for complex nouns like "диван-кровать"
            templates_list.append(obj.name[7:]) # without the part "Шаблон:"
            
    return(templates_list)


def stems(site, word, set_with_redirections):
    """
    Given a word, returns a set with tuples (stem, template, variable_name).
    There are usually one or two stems, but may be more.
    Variable name is how the stem is called: основа, основа1 etc.
    "set_without_templates" collects words without any templates
    (instead of printing this information as an output).
    "set_with_redirections" collects words whose templates are redirected.
    """
    page = site.Pages[word]
    templates_list = templates(site, word)
    text = page.text()
    if isinstance(text, dict):
        text = text['*'] # cause in some cases page.text is an ordered dict, not a string
    stems_list = []
    length = len(templates_list)
    
    if length > 1: # if there are several templates for one word
        sub_texts_dict = {} # keys - templates, values - substrings of the initial text
        # containing text chunks with the corresponding template and its stems
        for i,template in enumerate(templates_list):
            try:
                start = text.index(template)
                end = start + 200 # cause stems are straight after the template name
                sub_texts_dict[template] = text[start:end]

            except IndexError: # if end is further than the end of the string
                print("Index Error in 'stems' -> text after template %s for the word %s is short" % (template, word))
                sub_texts_dict[template] = text[start:]

            except ValueError: # if page text does not contain the template name (most probably due to redirection)
                # print("Value Error in 'stems' -> text for the word %s does not contain the template %s" % (word, template))
                # we've already got this
                set_with_redirections.add(word)
                new_page = site.Pages["Шаблон:"+template]
                new_text = new_page.text()

                # THE FOLLOWING DOESN'T WORK, cause the template that is not in the page's text is not the one that
                # is being redirected, but rather the one to which another one is redirected. E.g. "подмастерье"
                # has two templates: Шаблон:сущ ru m a (n 6*a(2)) and Шаблон:сущ ru n a 6*a(2)-m. The page's text
                # contains only the second one, but the second one is redirected to the first one when opened
                if "перенаправление" in new_text: # if it's not in new_text, we do nothing
                    print("The above Value Error is due to redirection")
                    # then the text most probably looks like "#перенаправление [[Шаблон:сущ ru m ina (c3*a(1))]]"
                    new_template = text[text.index("перенаправление")+15:].strip().strip("[").strip("]")
                    new_template = new_template[7:]
                    if new_template in temlpates_list: # then we have already seen or will see it
                        continue
                    else:
                        try:
                            start = text.index(new_template)
                            end = start + 200 # cause stems are straight after the template name
                            sub_texts_dict[new_template] = text[start:end]
                        except IndexError: # if end is further than the end of the string
                            sub_texts_dict[new_template] = text[start:]
                            print("Index Error in 'stems' for the word %s with THE NEW TEMPLATE %s" % (word, template))
                
        for template in sub_texts_dict:
            text = sub_texts_dict[template]
            add_triples(site, text, template, stems_list)
             
    elif length == 1:
        template = templates_list[0]
        add_triples(site, text, template, stems_list)

    elif length == 0:
        # we've already got this
        # set_without_templates.add(word)
        pass

    return(set(stems_list)) # if templates list is empty than stems_list is also empty


def add_triples(site, text, template, stems_list):
    """
    Returns a list with added triples (stem, variable_name, template), given:
    1) a text where to look for the variable name (i.e. for the word "основа"),
    2) a template name, and
    3) the list where to add triples and which will be returned.
    """
    index = 0
    while True:
        # the data may be without spaces like "основа=дру́г\n|основа1=друз\n|слоги="
        # or with them like here: "основа = беготн\n| основа1 = \n|слоги="
        try:
            # at each new step will look through a substring that starts where 
            # ended the word "основа" that we have found (i.e. start from "index+6")
            index = text.index("основа", index+6)
            
            # check that after the word "основа" there is "=" - so that it is not
            # part of the word "основанный", for example.
            while True:
                try:
                    # make sure that this is not a word like "основанный"
                    boolean = text[index+6]=="=" or text[index+7]=="=" or text[index+8]=="="
                except IndexError: # string index out of range
                    try:
                        boolean = text[index+6]=="=" or text[index+7]=="="
                    except IndexError:
                        try:
                            boolean = text[index+6]=="="
                        except IndexError:
                            boolean = False
        
                if boolean: # means that this is the right "основа"
                    break
                else: # means that "основа" was part of another word
                    # so we skip this "основа" by moving 6 chars to the right
                    index = text.index("основа", index+6)
                    
            variable_name = text[index:text.index("=", index)].strip()
            stem = text[text.index("=", index)+1:text.index("\n",  index)].strip()
            stem = stem.replace('\u0301','').replace('\u0300','').lower().strip() # delete stress symbols
            if stem != '': # if it is empty we do not include into our db
                stems_list.append((stem, template, variable_name))
                
        except ValueError: # when there are no more words 'основа' in the rest of the file
            break
        
    return(stems_list)


def flections(site, template):
    """
    Returns a dict with keys: "основа", "основа1" etc., where values are sets containing flections.
    """
    # (*) variation like acc-pl={{{основа1|{{{основа}}}и}}}(ref. "Шаблон:сущ ru f ina 6a", for example)
    # (**) variation like ins-sg={{{основа}}}о́й,<br>{{{основа}}}о́ю
    # (***) variation case like {{{основа}}}а <br />{{{основа}}}ы
    
    page = site.Pages["Шаблон:"+template]
    text = page.text()
    
    if "перенаправление" in text:
        # then the text most probably looks like "#перенаправление [[Шаблон:сущ ru m ina (c3*a(1))]]"
        new_template = text[text.index("перенаправление")+15:].strip().strip("[").strip("]")
        page = site.Pages[new_template]
        
    if isinstance(text, dict):
        text = text['*'] # cause in some cases page.text is an ordered dict, not a string
        
    text = page.text().split("\n")
        
    return_dict = {}
    for chunk in text: # look at each line of the text
        if "основа" in chunk:
            chunk = chunk.replace("&nbsp;","").replace("br","|").replace("<","|").replace(",","|").replace("//","|")
            if "|" in chunk[1:]: # [1:] cause the first char is usually "|" anyway
                chunk = chunk.split("|") # need to work with the variation cases *, **, and ***
            else:
                chunk = [chunk]

            # now we have lists instead of strings
            for subchunk in chunk:
                try:
                    start = subchunk.index("основа")
                    try:
                        next_char = subchunk[start+6]
                        if next_char.isdigit:
                            variable_name = "основа" + next_char
                        else:
                            variable_name = "основа"
                    except IndexError: # if there are no next symbol after "основа" in the subchunk
                        variable_name = "основа"
                    return_dict.setdefault(variable_name, set())
                except ValueError: # if subchunk doesn't contain 'основа', like the first one here:
                    continue # nom-pl={{incorrect | {{{основа1}}}ы}}

                # now we have variable_name ONLY IF THERE WAS NO ERROR and are in the subchunk that also contains a flection
                flection = subchunk[subchunk.index(variable_name)+len(variable_name):].strip()
                flection = flection.replace("}","").replace("{","").replace(">","").strip()
                
                flection = flection.replace('\u0301','').replace('\u0301','').lower() # delete stress symbols and to the lower case
                flection = flection.replace("основа","") # otherwise there are flections like "=основа-22"

                return_dict[variable_name].add(flection)

    return(return_dict)


def create_stems_db(db_name, file_with_words):
    """
    Creates a database where stems are keys and values are inner dicts. The inner dicts
    have tuples (template, variable_name) as keys and lemmas as values.
    """
    num_threads = 25
    thread_list = []
    with codecs.open(file_with_words, encoding = "utf-8") as file:
        # divide words in the file into ~equal groups to pass them to threads
        divided_file = divide_list(file.read().split("\n"), num_threads)

    set_with_redirections = set() # a set for words that do not have any templates
    online_dict = {}
    for i in range(num_threads):
        thread = Threads_for_stems_dict(online_dict, divided_file[i], set_with_redirections)
        thread_list.append(thread)
        thread.start()
        
    for thread in thread_list:
        thread.join()

    # ЗАПИСЫВАЛИ СНАЧАЛА set_without_templates, ПОТОМ set_with_redirections
    with codecs.open("set_with_redirections.txt", 'w', encoding = "utf-8") as file:
        for word in set_with_redirections:
            file.write(word+"\n\r\n")
                    
    # now write the dict into the db
    with shelve.open(db_name, writeback=True) as db:
        for key in online_dict:
            db[key] = online_dict[key]
            
    return

    
def create_flections_db(db_name, file_with_templates):
    """
    Creates a database where flections are keys amd values are sets with tuples (template, variable_name).
    """
    num_threads = 25
    thread_list = []

    with codecs.open(file_with_templates, encoding = "utf-8") as file:
        # divide templates in the file into small groups for treads to work with them
        divided_file = divide_list(file.read().split("\n"), num_threads)

    online_dict = {}
    for i in range(num_threads):
        thread = Threads_for_flections_dict(online_dict, divided_file[i])
        thread_list.append(thread)
        thread.start()
        
    for thread in thread_list:
        thread.join()
            
    # now write the dict into the db
    with shelve.open(db_name, writeback=True) as db:
        for key in online_dict:
            db[key] = online_dict[key]
            
    return


def divide_list(whole_list,num_of_groups):
    """
    Divides given list into the given number of smaller list, returns list of these lists.
    The last list is often the smallest cause it contains the remainder.
    """
    divided_list = []
    items_per_group = round(len(whole_list)/num_of_groups)
    for i in range(num_of_groups):
        if i==num_of_groups-1: # the last list includes remainder of the division
            divided_list.append(whole_list[i*items_per_group:])
        else:
            divided_list.append(whole_list[i*items_per_group:(i+1)*items_per_group])
            
    return(divided_list)


if __name__ == "__main__":
    PATH = "C:\\Users\\Admin.Ann-s\\Python\\Python36-32\\_Программирование III\\"
    create_stems_db("new_stems_db", PATH+"all_words.txt")
    print("Done with the first db")
    #create_flections_db("flections_db", PATH+"all_templates.txt")
    #print("Done with the second db")
