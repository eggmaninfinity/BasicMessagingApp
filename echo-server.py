import socket

HOST = "0.0.0.0"  # listening on all IPv4(?) interfaces
PORT = 65432  # Port to listen on (non-privileged ports are > 1023)

connectedClients = {}

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    conn, addr = s.accept()

    with conn:
        login = conn.recv(1024)
        clientName = f"{login.decode()}"
        connectedClients[addr] = f"{clientName}"
        print(f"Connected by {connectedClients[addr]} @ {addr}")


        while True:
            data = conn.recv(1024)

            if not data:
                break
            
            print(f"Received: {data.decode()}")
            reply = input(f"Message: ")
            conn.sendall(reply.encode())

print(f"Connection closed by {addr}")

# TODO: server asks for name on connect, adds name to dict with IP (names deleted on quit?), lists other active users in dict, 
# client connects by typing in name (how does other client know to listen for conn from other client?)