import socket

HOST = "127.0.0.1"
PORT = 65432

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    print("Connected to server. Type'exit' to quit.\n")

    while True:
        #send message
        msg = input("Client: ")
        s.sendall(msg.encode())
        if msg.lower() == "exit":
            print("Closing Connection")
            break

        #recieve reply
        data = s.recv(1024).decode()
        if not data or data.lower() == "exit" :
            print("Server Disconnected")
            break
        print(f"Server: {data}")
        