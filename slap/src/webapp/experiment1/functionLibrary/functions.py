from http.server import BaseHTTPRequestHandler, HTTPServer
import json
with open('slap/src/webapp/experiment1/webpages/default.html', 'r') as read:
    html_default = read.read()
with open('slap/src/webapp/experiment1/webpages/getTime.html', 'r') as read:
    html_getTime = read.read()
with open('slap/src/webapp/experiment1/webpages/changeAngle.html', 'r') as read:
    html_changeAngle = read.read()

angle = 0
class SimpleSlapRequestHandler(BaseHTTPRequestHandler):
   
    
    def do_GET(self):
        print("recieved GET request")
        print(f"path: {self.path}")
        print(f"headers: {self.headers}")
        #Send a Response
        self.send_response(200)
        self.send_header("Content-Type", "text/html")
        # insert message
        match[self.path]:
            case["/"]:
                message = html_default
            case["/getTime"]:
                message = html_getTime
            case["/changeangle"]:
                message = html_changeAngle 


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
        if self.path == '/setDirection':
             content_length = int(self.headers.get('Content-length'))
             put_data = self.rfile.read(content_length)
             print(put_data.decode('utf-8'))
             print(type(put_data))
             print(put_data)
             angle += int(put_data)
             response_data = {"angle": angle}
             print("Set Direction", response_data)
             
             response_json = json.dumps(response_data)

             # Send HTTP headers
             self.send_response(200)
             self.send_header("Content-Type", "application/json")
             self.end_headers()

             # Send JSON data
             self.wfile.write(response_json.encode())

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