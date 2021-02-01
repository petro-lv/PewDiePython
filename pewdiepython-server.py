from http.server import BaseHTTPRequestHandler, HTTPServer
import logging
import json

from pewdiepython import User


class Image:
    def __init__(self, color, url):
        self.color = color
        self.url = url


class ImageEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Image):
            return {"color": obj.color, "url": obj.url}
        return json.JSONEncoder.default(self, obj)


class S(BaseHTTPRequestHandler):
    def _set_response(self):
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()

    def do_GET(self):
        logging.info("GET request,\nPath: %s\nHeaders:\n%s\n", str(self.path), str(self.headers))
        self._set_response()

        if self.path.startswith('/analyze'):
            username = self.path.split('/')[-1]
            user = User(username)
            colors = user.analyze()
            print(colors)
            self.wfile.write(json.dumps(colors).encode('utf-8'))

        elif self.path.startswith('/user-analyze'):
            username = self.headers['Insta-Username']
            password = self.headers['Insta-Password']



    # def do_POST(self):
    #     content_length = int(self.headers['Content-Length']) # <--- Gets the size of data
    #     post_data = self.rfile.read(content_length) # <--- Gets the data itself
    #     logging.info("POST request,\nPath: %s\nHeaders:\n%s\n\nBody:\n%s\n",
    #             str(self.path), str(self.headers), post_data.decode('utf-8'))
    #
    #     self._set_response()
    #     self.wfile.write("POST request for {}".format(self.path).encode('utf-8'))

def run(server_class=HTTPServer, handler_class=S, port=8080):
    logging.basicConfig(level=logging.INFO)
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    logging.info('Starting httpd...\n')
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()
    logging.info('Stopping httpd...\n')

if __name__ == '__main__':
    from sys import argv

    if len(argv) == 2:
        run(port=int(argv[1]))
    else:
        run()
