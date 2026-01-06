import socket
import threading

HOST = "0.0.0.0"  # listening on all IPv4(?) interfaces
PORT = 65535  # Port to listen on (non-privileged ports are > 1023)

connectedClients = {}

def main():
    
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        print("Waiting for connection")

        while True:
            conn, addr = s.accept()
            thread = threading.Thread(
                target=handle_client,
                args=(conn, addr)
            )
            thread.start()

def handle_client(conn, addr):
    login = conn.recv(1024)
    clientName = login.decode()

    connectedClients[addr] = clientName
    print(f"{clientName} connected from {addr}")

    while True:
        data = conn.recv(1024)
        if not data:
            break

        message = f"{data.decode()}"

        if message.lower() == "list users":
            clients = f"{connectedClients}"
            conn.sendall(clients.encode())
            continue
        
        print(f"{clientName}: {message}")
        conn.sendall(b"Message Received")
        

    print(f"{clientName} disconnected")
    del connectedClients[addr]
    conn.close()


if __name__ == "__main__":
    main()

# TODO: lists other active users in dict, 
# (for multi user: how does client know to listen for conn from other client?)