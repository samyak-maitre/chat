def send_message(sock, msg_type, payload):
    length = len(payload)
    header = length.to_bytes(4, "big") + msg_type.to_bytes(1, "big")
    sock.sendall(header + payload)

def recv_message(sock):
    header = sock.recv(5)
    if not header:
        return b""
    length = int.from_bytes(header[:4], "big")
    payload = b""
    while len(payload) < length:
        payload += sock.recv(length - len(payload))
    return payload
