import socket

# Setup client to connect to server
server_ip = '127.0.0.1'
server_port = 8080

# Create a socket object for the client
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect to the server
client_socket.connect((server_ip, server_port))
print(f"Connected to {server_ip}:{server_port}")

# test sending data
message = "Hello, server!"
client_socket.send(message.encode('utf-8'))

# test response
data = client_socket.recv(1024)
print(f"Received data from server: {data.decode('utf-8')}")

client_socket.close()
