import my_indexer_combined
import search_engine_new
import os
import webbrowser

class Result(object):
    """
    Contains three methods:
    final_prog_from_files - if we want to create everything from scratch
                            we begin with indexing files and creating a db.
    final_prog_from_db - if we have a pre-created db and start to work with it.
    final_prog_with_limit_offset - for showing only a portion from documents
                            and a portion of citations for each documen on
                            the server.
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

        # here we create an html output in the 'output' variable
        
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

    def final_prog_with_limit_offset(self,engine,query,window_length,doc_limit,doc_offset,lim_off_list):
        """
        Returns an html output given:
        1) an engine instance (so we don't create it for each new query),
        2) a query as a string,
        3) a window length,
        4) how many documents to show on the page,
        5) starting from which document (here we count from 0), and
        6) a list of pairs (limit,offset), where each pair contains parameters how many citations and
           starting from which one to show on the page - for each corresponding document.
        """
        # here we don't need the 'lim_off_list' argument
        windows_dict = engine.get_context_for_words(query,int(window_length),doc_limit,doc_offset)
        result = engine.make_windows_sentences(windows_dict,lim_off_list)

        # here we create an html output in the 'output' variable
        final_dict = engine.make_dict_with_citations(result)
        output = []

        if final_dict == {}:
            output.append("Ooops, no more files to show! ") 
            return(''.join(output), 0, [])
        else:
            # the ordered list of files begins
            output.append("<ol>")
            
            numb_of_returned_citations_per_each_doc = []    
            for key in final_dict:
                numb_of_returned_citations_per_each_doc.append(len(final_dict[key]))  ### NEW
                output.append("<li><p><b>%s</b></p><ul>" % key)
                if final_dict[key] != []:
                    for string in final_dict[key]:
                        # each string with the answer is an item in an unordered list
                        output.append("<li>"+string+"</li>")
                    output.append("</ul></li>")
                else:
                    output.append("Ooops, no more citationis in this document! </ul></li>")
            # in the very end we close the ordered list        
            output.append("</ol>")
        
        return(''.join(output), len(final_dict), numb_of_returned_citations_per_each_doc)
