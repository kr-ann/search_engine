"""
Given a word, we find its stems, template, and template's flections.
"""

import mwclient as mw

site = mw.Site('ru.wiktionary.org')

def template(word):
    """
    Returns a template name, given a word as a string.
    """
    page = site.Pages[word]
    for obj in page.templates():
        if "Шаблон:сущ ru" in obj.name:
            return(obj.name)

def stems(word):
    """
    Returns a tuple with two stems. The second one may be an empty string.
    """
    page = site.Pages[word]
    substring = page.text()[:200] # the stems are in the beginning of the article
    try: # if there are no spaces like here: основа=дру́г\n|основа1=друз\n|слоги=
        first = substring[substring.find("основа=")+7:substring.find("основа1")-2]
        second = substring[substring.find("основа1")+8:substring.find("слоги")-2]
    except ValueError: # if there are spaces: основа = беготн\n| основа1 = \n|слоги=
        first = substring[substring.find("основа =")+8:substring.find("основа1")-3].strip()
        second = substring[substring.find("основа1 =")+9:substring.find("слоги")-3].strip()
    return((first, second))

def flections(template):
    """
    Returns a dict with two keys: "основа" and "основа1".
    Their values are also dicts, like {nom-sg: "", gen-sg: "а", ...}.
    The dict for "основа1" may be empty.
    """
    # here may be some irregularities, for instance:
    # two forms for a case, like 'ins-sg' and 'ins-sg2' (ей/ею) - then we include both of them.
    # there is 'loc-sg' but neither stem nor flection is written - such cases are not included.
    # variation (?) like acc-pl={{{основа1|{{{основа}}}и}}} - then we take the option with "основа",
    # because on the template page there is that option (ref. "Шаблон:сущ ru f ina 6a", for example)
    page = site.Pages[template]
    text = template.text().split("\n")
    return_dict = {"основа":{}, "основа1":{}}
    for chunk in text:
        if "{основа}" in chunk:
            case = chunk[1:chunk.find("=")]
            flection = chunk[chunk.find("{основа}")+10:].strip()
            return_dict["основа"][case]=flection
        if "{основа1}" in chunk:
            case = chunk[1:chunk.find("=")]
            flection = chunk[chunk.find("{основа1}")+11:].strip()
            return_dict["основа1"][case]=flection
    return(return_dict)
            
    
