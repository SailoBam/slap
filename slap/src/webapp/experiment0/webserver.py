from http.server import HTTPServer, SimpleHTTPRequestHandler
import os

class CustomRequestHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/":
            self.path = "/index.html"  # Serve the index.html file
            return super().do_GET()
        if self.path == '/sailo':
            # Insert your code here
            print("hello")



    #def do_GET(self):

     
     #   self.send_response(200)


if __name__ == "__main__":
    web_dir = os.path.join(os.path.dirname(__file__), "static")  # Directory containing index.html
    os.chdir(web_dir)  # Change working directory to serve files from
    server_address = ("", 8000)  # Listen on all available interfaces at port 8000
    httpd = HTTPServer(server_address, CustomRequestHandler)
    print("Server running on http://localhost:8000")
    httpd.serve_forever()

