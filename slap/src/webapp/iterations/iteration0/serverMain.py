from http.server import BaseHTTPRequestHandler, HTTPServer
import json
from functionLibrary.functions import SimpleSlapRequestHandler
import os

handler_class = SimpleSlapRequestHandler

def run(server_class = HTTPServer, handler_class = SimpleSlapRequestHandler, port = 8080):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print("Starting Server on port: " + str(port))
    httpd.serve_forever()

if __name__ == "__main__":
    print("Working Dir: " + os.getcwd())
    run()