from http.server import BaseHTTPRequestHandler
from http.server import HTTPServer
from random import randint
import os


class HttpGetHandler(BaseHTTPRequestHandler):

    def simple_template_engine(self, path, data):
        templating_data = {
            '/': {'randnum': randint(1, 10)}
        }
        if path in templating_data:
            return data % templating_data[path]
        else:
            return data


    def read_file_structure(self, path):
        sys_path = f'./static{path}' if path != '/' else './static/index.html'  # can be security breaches here
        if not os.path.isfile(sys_path):
            return False
        filename, extension = os.path.splitext(sys_path)
        with open(sys_path, 'rb') as file_to_send:
            if extension in ('.ico', '.jpg', '.png'):
                data_from_file = (file_to_send.read(), 'img')
            elif extension in ('.html', '.js', '.css', '.json', '.txt'):
                data_from_file = (file_to_send.read(), 'text')
            return data_from_file


    def do_GET(self):
        data_to_send = self.read_file_structure(self.path)
        if data_to_send:
            if data_to_send[1] == 'img':
                self.send_response(200)
                self.send_header("Content-Type", "image/x-icon")
                self.send_header("Content-Length", len(data_to_send[0]))
                self.end_headers()
                self.wfile.write(data_to_send[0])
            elif data_to_send[1] == 'text':
                data_to_send = self.simple_template_engine(self.path, data_to_send[0].decode())
                self.send_response(200)
                self.send_header("Content-type", "text/html")
                self.end_headers()
                self.wfile.write(data_to_send.encode())
        else:
            self.send_response(404)


def run(server_class=HTTPServer, handler_class=HttpGetHandler):
    server_address = ('', 8000)
    httpd = server_class(server_address, handler_class)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        httpd.server_close()


if __name__ == '__main__':
    run()
