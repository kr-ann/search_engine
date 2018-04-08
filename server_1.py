# https://docs.python.org/3/library/http.server.html

from http.server import BaseHTTPRequestHandler, HTTPServer
import cgi
import final_prog

class Serv(BaseHTTPRequestHandler):

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
<input type = \"text\" name = \"query\">
<input type = \"submit\" name = \"button\">
</form> </body> </html>""", encoding = "utf-8")
        self.wfile.write(first_html)

        
    def do_POST(self):
        self._set_headers()
        form = cgi.FieldStorage(fp=self.rfile,
                                headers=self.headers,
                                environ={'REQUEST_METHOD':'POST'},
                                )
        
        query = form.getvalue('query')
        print("ЗАПРОС:", str(query))      
        

        self.wfile.write(bytes("""
<html>
<body>
<form action = "" method = "post">
<input type = \"text\" name = \"query\" value = "%s">
<input type = \"submit\" name = \"button\">
</form>
""" % query, encoding = "utf-8"))

        # here we get text fragments in an html format
        # they are got from the previous programms
        text = final_prog.Result().final_prog_from_db("war_and_peace",str(query),3)
        self.wfile.write(bytes(text, encoding = "utf-8"))
        self.wfile.write(bytes("</body> </html>", encoding = "utf-8"))

    
def run(server_class=HTTPServer, handler_class=Serv, port=8000):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print('Starting httpd...')
    httpd.serve_forever()

run()
