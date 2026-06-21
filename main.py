import http.server, socketserver, json, urllib.request, threading, time, random, os
from urllib.error import URLError, HTTPError

PORT = 8765
SEEK_TOKEN = "eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJzdWIiOiJBUy1YNkNZUiIsImF1ZCI6ImFpLXNlZWsiLCJwcm92aWRlciI6InV1aWQiLCJpc3MiOiJhaS1zZWVrIiwiZXhwIjoyMDkzMTk5ODY1LCJpYXQiOjE3Nzc4Mzk4NjV9.w2wlNLg2S-om4xqWmakO2tEUjiPjxtGwFozmoI217VUu7KGC1O3qaL7KdyEIBYrGxIZV3lMWospZPPgVOYJjOeDgKBFnhg1_7NRKfmCEum_0moUEqH6dGFtQUQixDi63k63wv6GhOs1Sorj6hLzdBxX6NHU6otOo6brls5UNYbc"
FIREBASE_KEY = "AIzaSyA27E7jUV8osRY7NzwP2fZwGoTkp5gJhZw"

# (انسخ هنا كامل الدوال الخاصة بك: call_seek_api, call_search_api, get_model_source, get_firebase_token)

class Handler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.send_response(200)
            self.send_header('Content-type', 'text/html; charset=utf-8')
            self.end_headers()
            with open('index.html', 'rb') as f: self.wfile.write(f.read())
        else: self.send_error(404)

    def do_POST(self):
        if self.path == '/chat':
            data = json.loads(self.rfile.read(int(self.headers['Content-Length'])))
            reply = call_seek_api(data['model'], data['prompt']) if get_model_source(data['model']) == "seek" else call_search_api(data['model'], data['prompt'])
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({'reply': reply}).encode())

if __name__ == "__main__":
    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        httpd.serve_forever()
