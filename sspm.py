from http.server import BaseHTTPRequestHandler
from http.server import HTTPServer
from random import randint
import mimetypes
import os
import sspm_config
import sqlite3
from functools import cached_property
import logging
import config
import urllib.parse
import json
import time
from http.cookies import SimpleCookie


class DBWorker:

    def __init__(self, database):
        self.connection = sqlite3.connect(database)
        self.cursor = self.connection.cursor()

    def create_tables(self):
        auth_user_creation = '''
        CREATE TABLE IF NOT EXISTS auth_user (
            userid INTEGER PRIMARY KEY AUTOINCREMENT,
            login TEXT,
            password TEXT
        );
        '''
        sspm_creds_creation = '''
        CREATE TABLE IF NOT EXISTS sspm_creds (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            userid INTEGER,
            creds_name TEXT,
            creds_login TEXT,
            creds_password TEXT
        );
        '''
        self.cursor.execute(auth_user_creation)
        self.cursor.execute(sspm_creds_creation)
        self.connection.commit()

    def chech_user_login_and_password(self, login, password):
        result = self.cursor.execute('''
        SELECT userid FROM auth_user WHERE login = ? AND password = ?;
        ''', (login, password)).fetchall()
        if not len(result):
            return None
        else:
            return result[0][0]

    def get_sspm_creds_by_userid(self, userid):
        result = self.cursor.execute('''
        SELECT creds_name, creds_login, creds_password from sspm_creds where userid = ?
        ''', (userid,)).fetchall()

        if not len(result):
            return None
        else:
            transformed_data = []
    
            for idx, (name, login, password) in enumerate(result, start=1):
                transformed_data.append({
                    "name": name,
                    "login": login,
                    "password": password
                })
            return transformed_data

    def __del__(self):
        self.connection.close()
        logging.info('DB is closed!')


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
        if self.path == '/checklogin':
            content_lenght = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_lenght)
            decoded_data = post_data.decode('utf-8')
            jsoned_data = json.loads(decoded_data)

            userid = db.chech_user_login_and_password(jsoned_data['unlock_login'],
                                                      jsoned_data['unlock_pass'])

            if userid:
                userid_json = json.dumps({"userid": str(userid)})
                self.send_response(200, 'Logged in')
                self.send_header('Content-type', 'application/json')
                self.send_header('Content-Length', len(userid_json))
                self.end_headers()
                self.wfile.write(userid_json.encode())
            else:
                self.send_response(401, 'Wrong creds')
                self.end_headers()
            # self.headers['login']
            # self.headers['password']
            # self.wfile.write()
        if self.path == '/get_creds':
            content_lenght = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_lenght)
            decoded_data = post_data.decode('utf-8')
            jsoned_data = json.loads(decoded_data)

            data_to_send = db.get_sspm_creds_by_userid(jsoned_data['userToken'])
            json_string_to_send = json.dumps(data_to_send)
            send_content_lenght = len(json_string_to_send)
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Content-Length', send_content_lenght)
            self.end_headers()
            self.wfile.write(json_string_to_send.encode())


def run(server_class=HTTPServer, handler_class=HttpGetHandler):
    server_address = ('', 8000)
    httpd = server_class(server_address, handler_class)
    logging.info('Init server...')
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        httpd.server_close()


if __name__ == '__main__':
    db = DBWorker(config.DB_NAME)
    db.create_tables()

    run()
