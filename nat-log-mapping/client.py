import socket

# Client IP, Server IP, and port
client_ip = '192.168.11.100'
server_ip = '127.0.0.2'  # Server IP that you want to connect to
server_port = 8080  # Server Port that you want to connect to

# Create a socket object
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    # Connect to the NAT firewall
    client_socket.connect(('127.0.0.2', 9090))

    # Send client IP, server IP, and server port to the firewall
    message = f"{client_ip}:{server_ip}:{server_port}"
    client_socket.send(message.encode())

    # Receive response from the firewall
    response = client_socket.recv(1024).decode()

    # User Login
    username = input("Enter your username: ")
    password = input("Enter your password: ")
    auth_message = f"AUTH:{username}:{password}"
    client_socket.send(auth_message.encode())

    if response == "Connection blocked by NAT firewall.":
        print("Connection blocked by the firewall")
    else:
        print(response)

        while True:
            data = input("Enter data to send to the server (or 'Q' to quit): ")
            client_socket.send(data.encode())
            if data.upper() == 'Q':
                break

except ConnectionRefusedError:
    print("Connection to the firewall refused. Please make sure the firewall is running.")
except Exception as e:
    print(f"An error occurred: {e}")

finally:
    client_socket.close()
