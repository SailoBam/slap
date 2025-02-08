from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import os
angle = 0
class SimpleSlapRequestHandler(BaseHTTPRequestHandler):
    
    file_dir = os.path.join('slap', 'src', 'webapp', 'iterations', 'iteration0', 'html', 'webpages')
    
    def do_GET(self):
        print("received GET request")
        print(f"path: {self.path}")
        print(f"headers: {self.headers}")

        self.send_response(200)
        self.send_header("Content-Type", "text/html")
        print("self.path :" + self.path)
        # handling which page has been requested
        if self.path == "/":
            print("Path equals '/' ")
            file_path = os.path.join(self.file_dir, 'default.html')
            print("Default.html has been requested")
        else:
            file_path = os.path.join(self.file_dir, self.path[1:] + '.html')
            print(self.path +".html has been requested")

        # Opening and reading requested HTML file
        try:
            with open(file_path, 'r') as read:
                message = read.read()
        except FileNotFoundError:
            self.send_response(404)
            message = "<h1>404 Not Found</h1>"

        self.send_header("Content-Length", str(len(message)))
        self.end_headers()
        self.wfile.write(message.encode("utf-8"))
        self.send_header("Content-Length", str(len(message)))
        self.send_header("User-Information", "Fetching module X. Please wait")
        self.end_headers()
        self.wfile.write(message.encode('utf-8'))

    def do_POST(self):
        print("recieved POST request")
        print(f"path: {self.path}")
        print(f"headers: {self.headers}")
        content_length = int(self.headers.get('Content-length'))
        post_data = self.rfile.read(content_length)
        print(post_data.decode('utf-8'))
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_PUT(self):
        global angle
        print(f"Received PUT request: {self.path}")
        
        # Instantiate the PathHandler class
        path_handler = PathHandler()
        
        # Call the setDirection method from PathHandler
        if self.path == '/addDirection':
            path_handler.addDirection(self)
        elif self.path == '/setDirection':
            path_handler.setDirection(self)

      
class PathHandler():

    def addDirection(self, handler):
        content_length = int(handler.headers.get('Content-length'))
        put_data = handler.rfile.read(content_length)
        print(put_data.decode('utf-8'))

        global angle  # Use the global angle variable
        angle += int(put_data.decode('utf-8'))  # Update the angle value
        
        response_data = {"angle": angle}
        print("Set Direction", response_data)
        
        response_json = json.dumps(response_data)

        # Send HTTP headers
        handler.send_response(200)
        handler.send_header("Content-Type", "application/json")
        handler.end_headers()

        # Send JSON data
        handler.wfile.write(response_json.encode())
        
    def setDirection(self, handler):
        content_length = int(handler.headers.get('Content-length'))
        put_data = handler.rfile.read(content_length)
        print(put_data.decode('utf-8'))

        global angle  # Use the global angle variable
        angle = int(put_data.decode('utf-8'))  # Update the angle value
        
        response_data = {"angle": angle}
        print("Set Direction", response_data)
        
        response_json = json.dumps(response_data)

        # Send HTTP headers
        handler.send_response(200)
        handler.send_header("Content-Type", "application/json")
        handler.end_headers()

        # Send JSON data
        handler.wfile.write(response_json.encode())