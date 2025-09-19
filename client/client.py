#ship proxy

import socket
import threading
import queue
from http.server import BaseHTTPRequestHandler, HTTPServer
from io import BytesIO
from utils import send_message, recv_message

OFFSHORE_HOST = "offshore-proxy"
OFFSHORE_PORT = 9999
TCP_CONN = None
REQUEST_QUEUE = queue.Queue()

def tcp_connect():
    global TCP_CONN
    TCP_CONN = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    TCP_CONN.connect((OFFSHORE_HOST, OFFSHORE_PORT))
    print(f"[CLIENT] Connected to offshore proxy at {OFFSHORE_HOST}:{OFFSHORE_PORT}")

def process_queue():
    while True:
        client_handler, raw_request = REQUEST_QUEUE.get()
        send_message(TCP_CONN, 0, raw_request)
        response_bytes = recv_message(TCP_CONN)
        client_handler.wfile.write(response_bytes)
        REQUEST_QUEUE.task_done()

class ProxyHandler(BaseHTTPRequestHandler):
    def do_CONNECT(self):
        self.send_response(200, "Connection Established")
        self.end_headers()
        REQUEST_QUEUE.put((self, self.raw_requestline + b"\r\n" + self.headers.as_bytes()))

    def do_GET(self): self._queue_request()
    def do_POST(self): self._queue_request()
    def do_PUT(self): self._queue_request()
    def do_DELETE(self): self._queue_request()

    def _queue_request(self):
        raw_request = self.raw_requestline + b"\r\n" + self.headers.as_bytes()
        if "Content-Length" in self.headers:
            raw_request += self.rfile.read(int(self.headers["Content-Length"]))
        REQUEST_QUEUE.put((self, raw_request))

if __name__ == "__main__":
    tcp_connect()
    threading.Thread(target=process_queue, daemon=True).start()
    server = HTTPServer(("0.0.0.0", 8080), ProxyHandler)
    print("[CLIENT] Ship proxy running on port 8080...")
    server.serve_forever()
