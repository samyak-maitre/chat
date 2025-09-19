# utils.py
import struct

def send_message(sock, msg_type: int, payload: bytes):
    """Send a message over TCP: 4-byte length + 1-byte type + payload"""
    length = len(payload)
    header = struct.pack(">I", length) + struct.pack("B", msg_type)
    sock.sendall(header + payload)

def recv_message(sock):
    """Receive a single message"""
    header = b""
    while len(header) < 5:
        chunk = sock.recv(5 - len(header))
        if not chunk:
            return None, None
        header += chunk
    length = struct.unpack(">I", header[:4])[0]
    msg_type = header[4]
    payload = b""
    while len(payload) < length:
        chunk = sock.recv(length - len(payload))
        if not chunk:
            return None, None
        payload += chunk
    return msg_type, payload
