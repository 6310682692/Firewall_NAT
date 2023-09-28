import socket

# Firewall Section

allowed_ip = ["127.0.0.1", "192.168.11.147", "192.168.11.167"]
denied_ip = ["127.0.0.1"]

def is_allow(ip):
    return ip in allowed_ip

def is_denied(ip):
    return ip in denied_ip

# Setup Socket Server
server_ip = '192.168.11.147'
server_port = 8080

# Create a socket object
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
 
# Bind the socket to the server address
server_socket.bind((server_ip, server_port))

# Setup connection
server_socket.listen(1)

print(f"Server is listening on {server_ip}:{server_port}")

# Handle Connection
while True:
    # Accept incoming connections
    client_socket, client_address = server_socket.accept()
    client_ip = client_address[0]

    # IP testing Here
    if is_denied(client_ip):
        print(f"Connection not allowed from {client_ip}:{client_address[1]}")
        client_socket.close()

    if is_allow(client_ip):
        while True:
            data = client_socket.recv(1024)
            if data.decode('utf-8') == 'q':
                print(f"Client in this ip has leave {client_ip}:{client_address[1]}")
                client_socket.close()
                break
            print(f"Data sent from {client_ip}:{client_address[1]}")
            print(f"Recive data : {data.decode('utf-8')}")

    else:
        print(f"Connection from unknown IP {client_ip}:{client_address[1]}")
        client_socket.close()  

