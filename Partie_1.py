from http.server import HTTPServer, BaseHTTPRequestHandler
import json

class SimpleHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/motd":
            self.send_response(200)
            self.send_header('Content-type', 'application/json; charset=utf-8')
            self.end_headers()
            response = {"motd": "Bienvenue sur CanaDuck !"}
            self.wfile.write(json.dumps(response).encode())
        else:
            self.send_response(404)
            self.send_header('Content-type', 'application/json; charset=utf-8')
            self.end_headers()
            self.wfile.write(json.dumps({"error": "Page not found"}).encode())

    def do_POST(self):
        if self.path == "/nick":
            content_length = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(content_length)
            try:
                data = json.loads(body)
                pseudo = data.get("pseudo")
                if isinstance(pseudo, str) and pseudo.strip():
                    if not hasattr(self.server, "pseudos"):
                        self.server.pseudos = {}
                    self.server.pseudos[self.client_address] = pseudo
                    self.send_response(200)
                    self.send_header('Content-type', 'application/json; charset=utf-8')
                    self.end_headers()
                    self.wfile.write(json.dumps({"status": "ok", "pseudo": pseudo}).encode())
                else:
                    self.send_response(400)
                    self.send_header('Content-type', 'application/json; charset=utf-8')
                    self.end_headers()
                    self.wfile.write(json.dumps({"error": "Invalid pseudo"}).encode())
            except Exception:
                self.send_response(400)
                self.send_header('Content-type', 'application/json; charset=utf-8')
                self.end_headers()
                self.wfile.write(json.dumps({"error": "Malformed JSON"}).encode())

        elif self.path == "/msg":
            content_length = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(content_length)
            try:
                data = json.loads(body)
                sender = data.get("from")
                message = data.get("message")
                if isinstance(sender, str) and sender.strip() and isinstance(message, str) and message.strip():
                    if not hasattr(self.server, "messages"):
                        self.server.messages = []
                    self.server.messages.append({"from": sender, "message": message})
                    self.send_response(201)
                    self.send_header('Content-type', 'application/json; charset=utf-8')
                    self.end_headers()
                    self.wfile.write(json.dumps({"status": "created"}).encode())
                else:
                    self.send_response(400)
                    self.send_header('Content-type', 'application/json; charset=utf-8')
                    self.end_headers()
                    self.wfile.write(json.dumps({"error": "Invalid data"}).encode())
            except Exception:
                self.send_response(400)
                self.send_header('Content-type', 'application/json; charset=utf-8')
                self.end_headers()
                self.wfile.write(json.dumps({"error": "Malformed JSON"}).encode())
        else:
            self.send_response(404)
            self.send_header('Content-type', 'application/json; charset=utf-8')
            self.end_headers()
            self.wfile.write(json.dumps({"error": "Page not found"}).encode())

if __name__ == '__main__':
    server_address = ('', 8080)
    httpd = HTTPServer(server_address, SimpleHandler)
    print("Serving on port 8080...")
    httpd.serve_forever()
