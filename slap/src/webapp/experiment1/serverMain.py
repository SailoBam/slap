from http.server import BaseHTTPRequestHandler, HTTPServer
import json
from functionLibrary.functions import SimpleSlapRequestHandler

handler_class = SimpleSlapRequestHandler
def run(server_class = HTTPServer, handler_class = SimpleSlapRequestHandler, port = 8080):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print("Starting Server")
    httpd.serve_forever()

if __name__ == "__main__":
    run()
