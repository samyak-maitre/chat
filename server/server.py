import socket
import http.client
from utils import send_message, recv_message

def handle_request(data):
    try:
        request_line, headers_alone = data.split(b"\r\n", 1)
        method, path, version = request_line.decode().split()
        host = None
        for line in headers_alone.decode().split("\r\n"):
            if line.lower().startswith("host:"):
                host = line.split(":", 1)[1].strip()
                break

        if not host:
            return b"HTTP/1.1 400 Bad Request\r\n\r\nMissing Host header"

        conn = http.client.HTTPConnection(host, 80, timeout=10)
        conn.request(method, path, headers={})
        resp = conn.getresponse()
        response_data = f"HTTP/1.1 {resp.status} {resp.reason}\r\n".encode()
        for header, value in resp.getheaders():
            response_data += f"{header}: {value}\r\n".encode()
        response_data += b"\r\n" + resp.read()
        conn.close()
        return response_data

    except Exception as e:
        return f"HTTP/1.1 500 Internal Server Error\r\n\r\n{e}".encode()

def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(("0.0.0.0", 9999))
    server.listen(1)
    print("[SERVER] Offshore proxy listening on port 9999...")
    conn, addr = server.accept()
    print(f"[SERVER] Ship connected from {addr}")

    while True:
        request_bytes = recv_message(conn)
        if not request_bytes:
            break
        response = handle_request(request_bytes)
        send_message(conn, 1, response)

if __name__ == "__main__":
    start_server()
