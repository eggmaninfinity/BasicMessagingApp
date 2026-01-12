import socket
import threading
import os
from prompt_toolkit import PromptSession
from prompt_toolkit.history import InMemoryHistory

# Fallback to 127.0.0.1 if not in Docker
HOST = os.getenv("SERVER_HOST", "127.0.0.1") 
PORT = 65535

session = PromptSession(history=InMemoryHistory())

def main():

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        print("Connected. Type 'quit' to exit")

        login = input("Your Name: ")
        s.sendall(login.encode())
        
        thread = threading.Thread(target=receiveMessages, args=(s,), daemon=True)
        thread.start()

        while True:
                try:
                    message = session.prompt("Message: ")
                    

                    if message.lower() == "quit":
                        break
                
                    s.sendall(message.encode())

                except KeyboardInterrupt:
                    break
            
def receiveMessages(sock):
    while True:
        try:
            data = sock.recv(1024)

            if not data:
                break
            
            print(f"\n{data.decode()}", end="\nMessage: ")
        
        except:
            break

if __name__ == "__main__":
    main()


# TODO import argparse for cli definition of server ip and port