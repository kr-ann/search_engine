import my_indexer_combined
import search_engine
import os
import webbrowser

class Result(object):
    """
    Contains two methods:
    final_prog_from_files - if we want to create everything from scratch
                            we begin with indexing files and creating a db.
    final_prog_from_db - if we have a pre-created db and start to work with it.
    """
    def final_prog_from_files(self,input_list,query,window_length):
        """
        Returns an html output as a string, given:
        1) a list of files where to search (input_list),
        2) a query as a string, and
        3) a window length.
        """
        
        ind = my_indexer_combined.Indexer()
        for file in input_list:
            try:
                ind.create_db_index('test_db', file)
            except FileNotFoundError:
                print("Файл не найлен", file)
                continue
    
        engine = search_engine.Engine('test_db')
        windows_dict = engine.get_context_for_words(query, int(length))
        result = engine.make_windows_sentences(windows_dict)

        # here we create an html output and write it to a FILE
        with open("html_file1.html", "w", encoding="utf-8") as f:
            final_dict = engine.make_dict_with_citations(result)
            output = []
            
            # for the server task we don't need the next line
            #output.append("<html><head><title>RESULT</title></head><body>")

            if final_dict != {}:
                # the ordered list of files begins
                output.append("<ol>")
                
            for key in final_dict:
                output.append("<li><p><b>%s</b></p><ul>" % key)
                for string in final_dict[key]:
                    # each string with the answer is an item in an unordered list
                    output.append("<li>"+string+"</li>")
                output.append("</ul></li>")
            # in the very end we close the ordered list        
            output.append("</ol>")
        
            # for the server task we don't need the next line
            #output.append("</body></html>")
            f.write(''.join(output))
    
        #webbrowser.open_new_tab("html_file1.html")

        del engine
        #os.remove("test_db.bak")
        #os.remove("test_db.dat")
        #os.remove("test_db.dir")

        # here we open the file again and return what's in there
        with open("html_file1.html","r",encoding="utf-8") as f:
            text = f.read()
        return(text)

            
    def final_prog_from_db(self,input_db,query,window_length):
        """
        Returns an html output given:
        1) a pre-created database (input_db), i.e. its name or path as
           a string, without extension (!),
        2) a query as a string, and
        3) a window length.
        """
    
        engine = search_engine.Engine(input_db)
        windows_dict = engine.get_context_for_words(query, int(window_length))
        result = engine.make_windows_sentences(windows_dict)

        # here we create an html output in the 'output' VARIABLE
        
        final_dict = engine.make_dict_with_citations(result)
        output = []

        if final_dict != {}:
            # the ordered list of files begins
            output.append("<ol>")
                
        for key in final_dict:
            output.append("<li><p><b>%s</b></p><ul>" % key)
            for string in final_dict[key]:
                # each string with the answer is an item in an unordered list
                output.append("<li>"+string+"</li>")
            output.append("</ul></li>")   
        # in the very end we close the ordered list        
        output.append("</ol>")
        
        del engine
        
        return(''.join(output))

# THIS PART IS TO CHECK HOW THEY WORK
"""
print("Введите через пробел имена файлов, в которых хотите искать:")
input_str = input().strip()
input_list = input_str.split()
print("Введите запрос:")
query = input()
print("Введите длину окна:")
length = input()

res1 = Result().final_prog_from_files(input_list,query,length)
res2 = Result().final_prog_from_db("test_db",query,length)
print(res1==res2)
"""
