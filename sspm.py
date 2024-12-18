from http.server import BaseHTTPRequestHandler
from http.server import HTTPServer
from random import randint
import mimetypes
import os
import sspm_config
from functools import cached_property


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

        available_pages = {
            'vault': './vault',
            'login': './login'
        }

        original_path_file, original_path_extension = os.path.splitext(path)
        # sys_path = f'./static{path}' if original_path_extension else './static/index.html'  # can be security breaches here
        sys_path = f'./static{path}' if original_path_extension else f'./static{original_path_file}/index.html'  # can be security breaches here
        filename, extension = os.path.splitext(sys_path)
        if not os.path.isfile(sys_path):
            return False
        with open(sys_path, 'rb') as file_to_send:
            if extension in ('.ico', '.jpg', '.png', '.svg'):
                data_from_file = (file_to_send.read(), 'file', extension)
            elif extension in ('.html', '.js', '.css', '.json', '.txt'):
                data_from_file = (file_to_send.read(), 'text', extension)
            return data_from_file


    def do_GET(self):
        data_to_send = self.read_file_structure(self.path)
        if data_to_send:
            file_mimetype = sspm_config.sspm_mimetypes[data_to_send[2]]
            if data_to_send[1] == 'file':
                self.send_response(200)
                self.send_header("Content-Type", file_mimetype)
                self.send_header("Content-Length", len(data_to_send[0]))
                self.end_headers()
                self.wfile.write(data_to_send[0])
            elif data_to_send[1] == 'text':
                data_to_send = self.simple_template_engine(self.path, data_to_send[0].decode())
                self.send_response(200)
                self.send_header("Content-type", file_mimetype)
                self.end_headers()
                self.wfile.write(data_to_send.encode())
        else:
            self.send_response(404)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(b'<h1>404</h1><h2><a href="/">go back</a></h2>')

    def do_POST(self):
        self.send_response(200)


def run(server_class=HTTPServer, handler_class=HttpGetHandler):
    server_address = ('', 8000)
    httpd = server_class(server_address, handler_class)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        httpd.server_close()


if __name__ == '__main__':
    run()
