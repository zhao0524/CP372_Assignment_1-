import socket

HOST = '127.0.0.1'   # Server IP
PORT = 5000          # Server port

# Create socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect to server
client_socket.connect((HOST, PORT))

while True:
    message = input("You: ")

    client_socket.sendall(message.encode())

    data = client_socket.recv(1024)

    print("Server:", data.decode())

    if message.lower() == "exit":
        break

client_socket.close()