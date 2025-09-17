import socket

HOST = "127.0.0.1"
PORT = 65432

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST,PORT))
    s.listen()
    print(f"Server is listening on {HOST}:{PORT}...")

    conn, addr = s.accept()
    with conn:
        print("Connected by", addr)
        while True:
            #receive message from client
            data = conn.recv(1024).decode()
            if not data or data.lower() == "exit":
                print("Client disconnected")
                break
            print(f"Client: {data}")

            #send reply
            msg = input("Server: ")
            conn.sendall(msg.encode())
            if msg.lower() == "exit":
                print("closing connection")
                break