import socket

# Client IP Server IP and port
client_ip = '192.168.11.100'
server_ip = '127.0.0.2' #Server IP that want to connect
server_port = 8080 #Server Port that want to connect

# Create a socket object
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect to the NAT firewall
client_socket.connect(('127.0.0.2', 9090))

# Send client IP, server IP, and server port to the firewall
message = f"{client_ip}:{server_ip}:{server_port}"
client_socket.send(message.encode())

# Receive and print the response from the firewall
response = client_socket.recv(1024).decode()
print("Response from firewall:", response)

# Close the socket
client_socket.close()
