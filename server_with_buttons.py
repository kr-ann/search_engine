# https://docs.python.org/3/library/http.server.html

from http.server import BaseHTTPRequestHandler, HTTPServer
import cgi
import final_prog
import search_engine_new

class Serv(BaseHTTPRequestHandler):
    """
    This class is for the server that shows results of our search.
    """

    def _set_headers(self):
        self.send_response(200) #Adds a response header to the headers buffer and logs the accepted request.
        self.send_header('Content-type', 'text/html;charset=utf-8')
        self.end_headers() # Adds a blank line (indicating the end of the HTTP headers in the response) 
        
    def do_GET(self):
        self._set_headers()
        first_html = bytes("""
<html>
<body>
<form action = "" method = "post">
QUERY:
<input type = \"text\" name = \"query\">
<input type = \"submit\" name = \"button_submit\" value = "submit">
<p>document limit:
<input type = \"text\" name = \"doc_limit\">
<input type = \"hidden\" name = \"doc_offset\">
<p><input type = \"submit\" disabled=\"disabled\" name = \"button_next\" value = "next">
<input type = \"submit\" disabled=\"disabled\" name = \"button_back\" value = "back">
<input type = \"submit\" disabled=\"disabled\" name = \"button_to_beginning\" value = "to beginning">
</form> </body> </html>""", encoding = "utf-8")
        self.wfile.write(first_html)

        
    def do_POST(self):
        self._set_headers()
        form = cgi.FieldStorage(fp=self.rfile,
                                headers=self.headers,
                                environ={'REQUEST_METHOD':'POST'},
                                )
        submit = form.getvalue('button_submit')
        next_ = form.getvalue('button_next')
        disabled_for_next = "" # this means that this button will be shown
        back = form.getvalue('button_back')
        to_beginning = form.getvalue('button_to_beginning')
        
        query = form.getvalue('query')
        if (type(query) != str):
            raise ValueError("Query is empty.")
        print("ЗАПРОС:", query)
        
        doc_l = form.getvalue('doc_limit')
        doc_o = form.getvalue('doc_offset')
        
        if submit is not None or to_beginning is not None:
            doc_o = 0 # in the beginning it should be zero
            
        # set default values in case the fields are empty
        if doc_l == None:
            doc_l = 4
        if doc_o == None:
            doc_o = 0 
        
        # check that input values are correct
        try:
            doc_limit = int(doc_l)
            doc_offset = int(doc_o)
        except ValueError:
            raise ValueError("Limits and offsets must be integers, query must be a string")
            
        # if the button has been pressed
        if next_ is not None:
            doc_offset += doc_limit
        if back is not None:
            doc_offset -= doc_limit

        # if we are on the first page - the buttons won't be shown
        if doc_offset == 0:
            disabled_for_back = " disabled = \"disabled\""
            disabled_for_to_beginning = " disabled = \"disabled\""
        else:
            disabled_for_back = ""
            disabled_for_to_beginning = ""

        if doc_limit>0 and doc_offset>=0:
            page_numb = (doc_offset//doc_limit)+1 # integer part
        else:
            raise ValueError("doc_limit must be > 0, doc_offset must be >= 0")

        # lists that will contain info whether the buttons should be disabled (for citations in each document)
        list_disabled_for_next = []
        list_disabled_for_back = []
        list_disabled_for_to_beginning = []
        # create list with limits and offsets for citations in documents
        i=0
        lim_off_list = []
        while i < doc_limit:
            number = str(i+1)
            lim_for_i = form.getvalue("cit_limit_"+number)
            off_for_i = form.getvalue("cit_offset_"+number)
            next_for_i = form.getvalue("button_next_cit_"+number) # whether the 'next' button has been pressed
            #try:
            #    list_disabled_for_next[i] = "" # at the beginning we can press it
            #except IndexError: # if there's no value yet
            list_disabled_for_next.append("")
            back_for_i = form.getvalue("button_back_cit_"+number)
            to_beginning_for_i = form.getvalue("button_to_beginning_cit_"+number)
            
            # set default values
            if lim_for_i==None:
                lim_for_i = 10 
            if off_for_i==None:
                off_for_i = 0

            # check whether input values for doc_limit and doc_offset are correct
            try:
                lim_for_i = int(lim_for_i)
                off_for_i = int(off_for_i)
            except ValueError:
                raise ValueError("Limits and offsets for citations must be integers")

            # check if a button was pressed and alter the values correspondingly
            if to_beginning_for_i is not None:
                off_for_i = 0
            if next_for_i is not None:
                off_for_i += lim_for_i
            if back_for_i is not None:
                off_for_i -= lim_for_i

            # if we are on the first page - the buttons won't be shown
            if off_for_i == 0:
                #try:
                #    list_disabled_for_back[i] = " disabled = \"disabled\""
                #except IndexError:
                list_disabled_for_back.append(" disabled = \"disabled\"")
                #try:
                #    list_disabled_for_to_beginning[i] = " disabled = \"disabled\""
                #except IndexError:
                list_disabled_for_to_beginning.append(" disabled = \"disabled\"")
            else:
                list_disabled_for_back.append("")
                list_disabled_for_to_beginning.append("")
                
            # some more checking about correctness + add the values to the list
            if lim_for_i>0 and off_for_i>=0:
                page_numb_for_i = (off_for_i//lim_for_i)+1 # integer part
                lim_off_list.append((lim_for_i,off_for_i,page_numb_for_i))
            else:
                raise ValueError("for citations limits must be > 0, offsets must be >= 0")
                
            i+=1
            
        
        # we gonna need 'text' later, but 'numb_of_returned_docs' and 'numb_of_returned_citations_per_docs' - now
        text, numb_of_returned_docs, numb_of_returned_citations_per_docs = final_prog.Result().final_prog_with_limit_offset(self.server.engine,
                                                                                                                            str(query), 3, doc_limit,
                                                                                                                            doc_offset, lim_off_list)
        if numb_of_returned_docs < doc_limit: # if we are on the last page
            disabled_for_next = " disabled = \"disabled\""

        j = 0 # counter
        while j < len(numb_of_returned_citations_per_docs):
            if numb_of_returned_citations_per_docs[j] < lim_off_list[j][0]:
                list_disabled_for_next[j] = " disabled = \"disabled\""
            j+=1
            
        
        # create as many fields for citations limits and offsets as there are documents (doc_limit)
        # and for each document also three buttons
        i = 1
        html_lim_offs = []
        while i <= doc_limit:
            number = str(i)
            html_lim_offs.append("""
<p>citations limit for %s:
<input type = \"text\" name = "%s" value = "%s">
<input type = \"hidden\" name = "%s" value = "%s">
<input type = \"submit\"%s name = "%s" value = "next">
<input type = \"submit\"%s name = "%s" value = "back">
<input type = \"submit\"%s name = "%s" value = "to beginning">
Номер страницы по цитатам: %s
</p>
""" % (number, "cit_limit_"+number, lim_off_list[i-1][0], "cit_offset_"+number,\
       lim_off_list[i-1][1], list_disabled_for_next[i-1], "button_next_cit_"+number,\
       list_disabled_for_back[i-1], "button_back_cit_"+number, list_disabled_for_to_beginning[i-1],\
       "button_to_beginning_cit_"+number, lim_off_list[i-1][2]))
            i+=1
                
        # create html
        self.wfile.write(bytes("""
<html>
<body>
<form action = "" method = "post">
QUERY:
<input type = \"text\" name = \"query\" value = "%s">
<input type = \"submit\" name = \"button_submit\" value = "submit">
<p>document limit:
<input type = \"text\" name = \"doc_limit\" value = "%s">
<input type = \"hidden\" name = \"doc_offset\" value = "%s">
<p><input type = \"submit\"%s name = \"button_next\" value = "next">
<input type = \"submit\"%s name = \"button_back\" value = "back">
<input type = \"submit\"%s name = \"button_to_beginning\" value = "to beginning">
</p>
<p>Номер страницы по документам: %s </p>
""" % (query,doc_limit,doc_offset, disabled_for_next, disabled_for_back,
       disabled_for_to_beginning, page_numb), encoding = "utf-8"))
        self.wfile.write(bytes(''.join(html_lim_offs)+"</form>", encoding = "utf-8"))
        self.wfile.write(bytes(text, encoding = "utf-8"))
        self.wfile.write(bytes("</body> </html>", encoding = "utf-8"))

    
def run(server_class=HTTPServer, handler_class=Serv, port=8001):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    httpd.engine = search_engine_new.Engine("war_and_peace") # add here "engine" attribute to our server
    # now we don't create an Engine instance for each query 
    print('Starting httpd...')
    try:
        httpd.serve_forever()
    except: 
        del httpd.engine
        raise # will recreate the error but previously deleting the engine instance 

run()
