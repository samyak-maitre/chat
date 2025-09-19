# server/server.py
import socket
import threading
from server.utils import send_message, recv_message
import http.client
import ssl

HOST = "0.0.0.0"
PORT = 9999

def forward_request(req_bytes):
    """Parse HTTP request and forward to target server"""
    req_lines = req_bytes.split(b"\r\n")
    method, path, version = req_lines[0].decode().split()
    
    # Parse headers
    headers = {}
    i = 1
    while req_lines[i]:
        k, v = req_lines[i].decode().split(":", 1)
        headers[k.strip()] = v.strip()
        i += 1
    i += 1
    body = b"\r\n".join(req_lines[i:])
    
    # Handle CONNECT (HTTPS)
    if method.upper() == "CONNECT":
        host, port = path.split(":")
        port = int(port)
        return b"HTTP/1.1 200 Connection Established\r\n\r\n", host, port, True
    
    # HTTP request
    conn = http.client.HTTPConnection(headers.get("Host", path))
    conn.request(method, path, body, headers)
    resp = conn.getresponse()
    resp_bytes = f"HTTP/1.1 {resp.status} {resp.reason}\r\n".encode()
    for k, v in resp.getheaders():
        resp_bytes += f"{k}: {v}\r\n".encode()
    resp_bytes += b"\r\n" + resp.read()
    return resp_bytes, None, None, False

def handle_client(conn):
    while True:
        msg_type, payload = recv_message(conn)
        if msg_type is None:
            break
        if msg_type == 0:  # Request
            response, host, port, is_https = forward_request(payload)
            send_message(conn, 1, response)

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen(5)
print(f"[INFO] Offshore proxy listening on {HOST}:{PORT}")

while True:
    conn, addr = server.accept()
    print(f"[INFO] Connection from {addr}")
    threading.Thread(target=handle_client, args=(conn,), daemon=True).start()
