import socket

HOST = '127.0.0.1'   # Localhost
PORT = 5000          # Port to listen on

# Create socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind socket to address and port
server_socket.bind((HOST, PORT))

# Start listening
server_socket.listen(1)

print(f"Server listening on {HOST}:{PORT}")

# Accept client connection
conn, addr = server_socket.accept()
print(f"Connected by {addr}")

while True:
    data = conn.recv(1024)

    if not data:
        break

    message = data.decode()
    print("Client:", message)

    reply = input("Server reply: ")
    conn.sendall(reply.encode())

conn.close()
server_socket.close()