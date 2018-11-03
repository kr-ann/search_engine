#https://media.readthedocs.org/pdf/mwclient/latest/mwclient.pdf
import mwclient as mw
import threading
import time
import codecs

site = mw.Site('ru.wiktionary.org')

def get_list_of_subcategories_and_pages(root_category):
    start = time.time()
    subcategories_list = [root_category] # initially the list contains only the root
    pages_list = []
    for category in subcategories_list:
        for page in site.Pages[category]:
            if page.namespace == 14:
                subcategories_list.append(page.name)
            else: # here we add either word pages (namespace 0) or templates (namespace 10)
                if page.name not in pages_list:
                    pages_list.append(page.name)
    end = time.time()
    print("Time", end - start)
    print("Number of subcategories", len(subcategories_list))
    print("Number of pages", len(pages_list))
    return(subcategories_list, pages_list)

subcategories_list, pages_list = get_list_of_subcategories_and_pages("Категория:Русские существительные")
path = "C:\\Users\\Admin.Ann-s\\Python\\Python36-32\\_Программирование III\\"
with codecs.open(path + "subcategories.txt", 'w', encoding='utf-8') as f1:
    f1.write('\r\r\n'.join(subcategories_list))
with codecs.open(path + "all_words.txt", 'w', encoding='utf-8') as f2:
    f2.write('\r\r\n'.join(pages_list))
print("the data is written to the files")


"""
# НЕПОСРЕДСТВЕННЫЕ ПОДКАТЕГОРИИ КОРНЯ
['Категория:Русские существительные по грамматическому роду',
'Категория:Русские существительные по типу склонения',
'Категория:Неодушевлённые/ru',
'Категория:Одушевлённые/ru',
'Категория:Отвлечённые существительные/ru',
'Категория:Русские отглагольные существительные',
'Категория:Русские существительные с местным падежом',
'Категория:Русские существительные с разделительным падежом',
'Категория:Русские существительные со звательным падежом',
'Категория:Составные слова с раздельно склоняемыми частями',
'Категория:Субстантиваты/ru',
'Категория:Существительные на -иво',
'Категория:Существительные на -ость',
'Категория:Существительные на -ство',
'Категория:Существительные, склонение 8°c^',
'Категория:Формы существительных/ru',
'Категория:Pluralia tantum/ru',
'Категория:Singularia tantum/ru']
"""


