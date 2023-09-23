import socket

# Setup Socket Server
server_ip = '127.0.0.1'
server_port = 8080

# Create a socket object
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to the server address
server_socket.bind((server_ip, server_port))

# Setup connection
server_socket.listen(1)

print(f"Server is listening on {server_ip}:{server_port}")

# Accept Connect
client_socket, client_address = server_socket.accept()
print(f"Accepted connection from {client_address[0]}:{client_address[1]}")

# Handle Connection
while True:
    data = client_socket.recv(1024)
    if not data:
        break
    print(f"Received data: {data.decode('utf-8')}")

client_socket.close()
server_socket.close()

# Firewall Section