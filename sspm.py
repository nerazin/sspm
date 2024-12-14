from http.server import BaseHTTPRequestHandler
from http.server import HTTPServer
from random import randint


class HttpGetHandler(BaseHTTPRequestHandler):

    def read_file_structure(self):
        with open('./static/index.html') as html_file:
            self.static_data_to_send = html_file.read() % {'randnum': randint(1, 10)}


    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.read_file_structure()
        self.wfile.write(self.static_data_to_send.encode())


def run(server_class=HTTPServer, handler_class=HttpGetHandler):
    server_address = ('', 8000)
    httpd = server_class(server_address, handler_class)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        httpd.server_close()


if __name__ == '__main__':
    run()
