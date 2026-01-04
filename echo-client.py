import socket

HOST = "127.0.0.1"  # The server's hostname or IP address
PORT = 65432  # The port used by the server

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    print("Connected. Type 'quit' to exit")

    login = input("Your Name: ")
    s.sendall(login.encode())
    while True:

        message = input("Message: ")

        if message.lower() == "quit":
            break
        
        s.sendall(message.encode())
        data = s.recv(1024)
        print(f"Received: {data.decode()}")

