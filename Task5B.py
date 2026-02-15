#Chat Application
import socket
import threading
import base64
import tkinter as tk
from tkinter import simpledialog


HOST = "127.0.0.1"
PORT = 6060


def encrypt(text):
    return base64.b64encode(text.encode()).decode()


def decrypt(text):
    return base64.b64decode(text.encode()).decode()


class ChatGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Secure Chat App")
        self.root.geometry("500x420")

        self.username = simpledialog.askstring("Login", "Enter username:")
        if not self.username:
            exit()

        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((HOST, PORT))
        self.socket.send(encrypt(self.username).encode())

        self.build_ui()
        threading.Thread(target=self.receive_messages, daemon=True).start()
        self.root.mainloop()

    def build_ui(self):
        # Chat display area
        self.chat_area = tk.Text(self.root, state="disabled", wrap="word")
        self.chat_area.pack(padx=10, pady=(10, 5), fill="both", expand=True)

        # Bottom frame for input
        bottom_frame = tk.Frame(self.root)
        bottom_frame.pack(fill="x", padx=10, pady=5)

        self.entry = tk.Entry(bottom_frame)
        self.entry.pack(side="left", fill="x", expand=True, padx=(0, 5))
        self.entry.bind("<Return>", self.send_message)

        send_btn = tk.Button(bottom_frame, text="Send", width=8, command=self.send_message)
        send_btn.pack(side="right")

    def send_message(self, event=None):
        message = self.entry.get().strip()
        if message:
            self.socket.send(encrypt(message).encode())
            self.entry.delete(0, tk.END)

    def receive_messages(self):
        while True:
            try:
                encrypted_msg = self.socket.recv(1024).decode()
                message = decrypt(encrypted_msg)

                self.chat_area.config(state="normal")
                self.chat_area.insert(tk.END, message + "\n")
                self.chat_area.config(state="disabled")
                self.chat_area.see(tk.END)
            except:
                break


if __name__ == "__main__":
    ChatGUI()
