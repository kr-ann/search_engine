# https://docs.python.org/3/library/http.server.html

from http.server import BaseHTTPRequestHandler, HTTPServer

class Serv(BaseHTTPRequestHandler):

    def _set_headers(self):
        self.send_response(200) #Adds a response header to the headers buffer and logs the accepted request.
        self.send_header('Content-type', 'text/html;charset=utf-8')
        self.end_headers() # Adds a blank line (indicating the end of the HTTP headers in the response) 
        
    def do_GET(self):
        self._set_headers()
        self.wfile.write(bytes("<html><body><form><input type = \"text\"><input type = \"submit\"></form></body></html>", encoding = "utf-8"))
        
def run(server_class=HTTPServer, handler_class=Serv, port=80):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print('Starting httpd...')
    httpd.serve_forever()

run()
