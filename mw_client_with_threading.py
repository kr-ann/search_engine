import mwclient as mw
import threading
import time
import codecs

class MyThread(threading.Thread):
    def __init__(self, site, subcategory_name):
        self.site = site
        self.subcategory_name = subcategory_name
    
    def run(self):
        print(threading.currentThread().getName() + '\n')
        get_words(self.site, self.subcategory_name)

def get_words(site, subcategory_name):
    subcategories_list = [subcategory_name]
    words_list = []
    for category in subcategories_list:
        for page in site.Pages[category]:
            if page.namespace == 14:
                subcategories_list.append(page.name)
            else:
                if page.name not in words_list:
                    words_list.append(page.name)
                    
    path = "C:\\Users\\Admin.Ann-s\\Python\\Python36-32\\_Программирование III\\"
    with open(path + "words_from_threading.txt", 'a') as file:
        file.write('\r\n\n')
        file.write('\r\r\n'.join(words_list))
    print("Some new words are added to the file")

if __name__ == '__main__':
    start = time.time()
    site = mw.Site('ru.wiktionary.org')
    start = time.time()
    immediate_subcategories = []
    words_list = []
    for page in site.Pages["Категория:Русские существительные"]:
        if page.namespace == 14:
            immediate_subcategories.append(page.name)
        else:
            words_list.append(page.name)
    path = "C:\\Users\\Admin.Ann-s\\Python\\Python36-32\\_Программирование III\\"
    with codecs.open(path + "words_from_threading.txt", 'w', encoding='utf-8') as file:
        file.write('\r\r\n'.join(words_list))
    print("Initial words are added to the file.")

    for category in immediate_subcategories:
        thread = MyThread(site, category)
        thread.start()
    end = time.time()
    print("Time", end - start)
    
