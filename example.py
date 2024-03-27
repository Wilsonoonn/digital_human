from http.server import BaseHTTPRequestHandler, HTTPServer
import os

class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        if self.path == '/lip-sync':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)

            print(post_data) 
          
            video_path = '/Users/wilson/Desktop/test.mp4'

            try:
                self.send_response(200)
                self.send_header('Content-type', 'video/mp4')
                self.send_header('Access-Control-Allow-Origin','*')

                self.end_headers()

                with open(video_path, 'rb') as file:
                    self.wfile.write(file.read())
            except IOError:
                self.send_error(404, 'File Not Found: %s' % video_path)

def run(server_class=HTTPServer, handler_class=SimpleHTTPRequestHandler, port=8888):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print('Starting httpd on port {port}...')
    httpd.serve_forever()

if __name__ == "__main__":
    from sys import argv

    if len(argv) == 2:
        run(port=int(argv[1]))
    else:
        run()
