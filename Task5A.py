#Chat Application
import socket
import threading
import base64


HOST = "127.0.0.1"
PORT = 6060

clients = {}


def encrypt(text):
    return base64.b64encode(text.encode()).decode()


def decrypt(text):
    return base64.b64decode(text.encode()).decode()


def broadcast(message, sender):
    for client in clients:
        if client != sender:
            client.send(encrypt(message).encode())


def handle_client(client_socket):
    username = decrypt(client_socket.recv(1024).decode())
    clients[client_socket] = username
    print(f"{username} joined the chat")

    broadcast(f"{username} joined the chat", client_socket)

    try:
        while True:
            encrypted_msg = client_socket.recv(1024).decode()
            message = decrypt(encrypted_msg)
            broadcast(f"{username}: {message}", client_socket)
    except:
        pass
    finally:
        print(f"{username} left the chat")
        broadcast(f"{username} left the chat", client_socket)
        del clients[client_socket]
        client_socket.close()


def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen()

    print("Secure Chat Server running...")

    while True:
        client_socket, _ = server.accept()
        threading.Thread(
            target=handle_client,
            args=(client_socket,),
            daemon=True
        ).start()


if __name__ == "__main__":
    start_server()
