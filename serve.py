#!/usr/bin/env python3
"""
Simple CORS-enabled HTTP server for local development.
Serves from the current directory on port 8000.
"""

import http.server
import socketserver
import os

PORT = 8000

class CORSHandler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Cache-Control', 'no-cache')
        super().end_headers()

    def log_message(self, fmt, *args):
        # Suppress 304 noise; keep errors
        if args[1] not in ('304',):
            super().log_message(fmt, *args)

os.chdir(os.path.dirname(os.path.abspath(__file__)))  # serve from project root
with socketserver.TCPServer(("", PORT), CORSHandler) as httpd:
    print(f"Serving on http://localhost:{PORT}")
    print(f"Open: http://localhost:{PORT}/index.html")
    print(f"Press Ctrl+C to stop.")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nServer stopped.")
