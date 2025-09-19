# client/client.py
from http.server import BaseHTTPRequestHandler, HTTPServer
import socket
import threading
import queue
from server.utils import send_message, recv_message

OFFSHORE_HOST = "offshore_host_here"
OFFSHORE_PORT = 9999
LISTEN_PORT = 8080

request_queue = queue.Queue()
response_map = {}

tcp_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tcp_sock.connect((OFFSHORE_HOST, OFFSHORE_PORT))

def tcp_worker():
    while True:
        handler = request_queue.get()
        raw_request = handler.raw_requestline + b"".join(handler.headers.buffer) + b"\r\n" + (handler.rfile.read(int(handler.headers.get('Content-Length', 0))) if handler.command != 'GET' else b"")
        send_message(tcp_sock, 0, raw_request)
        msg_type, response = recv_message(tcp_sock)
        handler.wfile.write(response)

threading.Thread(target=tcp_worker, daemon=True).start()

class ProxyHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.queue_request()
    def do_POST(self):
        self.queue_request()
    def do_PUT(self):
        self.queue_request()
    def do_DELETE(self):
        self.queue_request()
    def do_CONNECT(self):
        self.send_error(501, "CONNECT not implemented yet")
    def queue_request(self):
        request_queue.put(self)

server = HTTPServer(('0.0.0.0', LISTEN_PORT), ProxyHandler)
print(f"[INFO] Ship proxy listening on port {LISTEN_PORT}")
server.serve_forever()
