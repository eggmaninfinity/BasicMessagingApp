import socket
import threading

HOST = "127.0.0.1"  # The server's hostname or IP address
PORT = 65535  # The port used by the server

def main():

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        print("Connected. Type 'quit' to exit")

        login = input("Your Name: ")
        s.sendall(login.encode())
        
        thread = threading.Thread(target=receiveMessages, args=(s,), daemon=True)
        thread.start()

        while True:
                message = input("Message: ")

                if message.lower() == "quit":
                    break
            
                s.sendall(message.encode())
            
def receiveMessages(sock):
    while True:
        try:
            data = sock.recv(1024)
            if not data:
                break
            print(f"\n{data.decode()}")
        
        except:
            break

if __name__ == "__main__":
    main()