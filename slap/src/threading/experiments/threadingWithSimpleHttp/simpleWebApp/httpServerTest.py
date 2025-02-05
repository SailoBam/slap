# HTTP Experiments
# I have written this code to build an understanding of HTTP requests and responses
# In the project I need to create a web server which will respond to user interactions such as changing the boats direction
# In this code I have a simple web server which responds to a GET and POST request.
# 

from http.server import BaseHTTPRequestHandler, HTTPServer
import json


angle = 100


# This is a simple request handler class to explore how to break down a HTTP request and create an appropriate response
class SimpleSlapRequestHandler(BaseHTTPRequestHandler):

    
   
# Process Dummy Paths from the http request
# I can test this in a browser or using curl as follows
# curl localhost:8080/getTime
    def do_GET(self):
        """ Description
        :type self:
        :param self:
    
        :raises:
    
        :rtype:
        :returns:
        """    
        print("recieved GET request")
        print(f"path: {self.path}")
        print(f"headers: {self.headers}")
        #Send a Response
        self.send_response(200)
        self.send_header("Content-Type", "text/html")
        message = """
            <html>
                <head><title>Unknown</title></head>
                <body>
                    <h1>Nothing</h1>
                    <button onclick="sendPostRequest()">Send POST Request</button>
                    <script>
                             function sendPutRequest() {
                const url = "https://example.com/api/resource"; // Replace with your API endpoint
                const data = {
                id: 123,
                name: "Updated Name",
                status: "active"
            };
                        
                    </script>
                </body>
            </html>
            """
        if self.path == '/get_direction':
            message = """
                <html>
                    <head><title>Change Value</title></head>
                    <body>
                        <div>
                            Angle = <div id = "angle">0</div>
                        </div>
                        <button onclick="changeValue(10)">Add 10</button>
                        <p id="value">Value: 0</p>
                        <script>      
                            function changeValue(c) {
                                const url = '/setDirection'; 
                                const data = c;
                                console.log("Inide changeValue", data)

                                fetch(url, {
                                    method: "PUT",
                                    headers: {
                                        "Content-Type": "text/html; charset=UTF-8"
                                    },
                                    body: JSON.stringify(data)
                                })
                                    .then(response => {
                                        if (!response.ok) {
                                            throw new Error(`HTTP error! status: ${response.status}`);
                                        }
                                        return response.json();
                                    })
                                    .then(data => {
                                        document.getElementById("angle").textContent = 
                                            "Success: " + data.angle;
                                    })
                                    .catch(error => {
                                        document.getElementById("angle").textContent = 
                                            "Error: " + error.message;
                                    });
                            }
                        </script>
                    </body>
                </html>
            """
        if self.path == '/getTime':
            message = "12:00:00"
        
   
        


        self.send_header("Content-Length", str(len(message)))
        self.send_header("User-Information", "Fetching module X. Please wait")
        self.end_headers()
        self.wfile.write(message.encode('utf-8'))
            
    
# Example POST method:
# curl -X POST -d "name = sailo" localhost:8080
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

    
def run(server_class = HTTPServer, handler_class = SimpleSlapRequestHandler, port = 8080):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print("Starting Server")
    httpd.serve_forever()

if __name__ == "__main__":
    run()
