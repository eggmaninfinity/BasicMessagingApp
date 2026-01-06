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
                args=(conn, addr),
                daemon=True
            )
            thread.start()

def handle_client(conn, addr):
    login = conn.recv(1024)
    clientName = login.decode()

    connectedClients[clientName] = conn
    print(f"{clientName} connected from {addr}")

    try:
        while True:
            data = conn.recv(1024)
            if not data:
                break

            message = f"{data.decode()}"

            if message.lower() == "list users":
                clients = ", ".join(connectedClients.keys())
                conn.sendall(clients.encode())
                continue

            if message.startswith("msg"):
                _, target, *text = message.split()
                text = " ".join(text)

                if target in connectedClients:
                    target_conn = connectedClients[target]
                    target_conn.sendall(
                        f"{clientName}: {text}".encode()
                    )
                    conn.sendall("Message Sent".encode())
                    continue

                else:
                    conn.sendall("\nuser not found".encode())
                    continue
            
            else:
                conn.sendall("unknown command".encode())
            
    finally:
        print(f"{clientName} disconnected")
        del connectedClients[clientName]
        conn.close()


if __name__ == "__main__":
    main()
