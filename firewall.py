import socket
import logging

# Firewall Function

def is_allow(ip):
    return ip in allowed_ip

def is_denied(ip):
    return ip in denied_ip

# Socket Init function
def open_server(gateway_ip, server_port):
    # Create a socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((gateway_ip, server_port))
    server_socket.listen(1)

    print(f"Server is listening on {gateway_ip}:{server_port}")

    return server_socket

# NAT Section
def NAT_Gate(client_socket, client_address, server_ip, server_port):
    # Connect nat to the server
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.connect((server_ip, server_port))

    # While Connected
    try:
        while True:
            data = client_socket.recv(1024)

            if not data:
                print(f"Client from this IP {client_address} has disconnected")
                response = "You have been disconnected"
                client_socket.send(response.encode('utf-8'))
                break

            if (data.decode('utf-8')).upper() == "Q":
                print(f"Client from this ip {client_address} has disconnected")
                response = "You have been disconnected"
                client_socket.send(response.encode('utf-8'))
                break

            # Sent Client data to server
            print(f"Data sent from {client_address}")
            print(f"Received data: {data.decode('utf-8')}")
            server_socket.send(data)

    except Exception as e:
        print(f"An error occurred: {e}")
        logging.error(f"An error occurred: {e}")

    finally:
        client_socket.close()
        server_socket.close()

def main():
    # Setup logging
    logging.basicConfig(filename='firewall_log.txt', level=logging.INFO, format='%(asctime)s - %(message)s')

    while True:
        # call server function
        server_socket = open_server(gateway_ip, server_port)
        try:
            # After client connect
            client_socket, client_address = server_socket.accept()
            client_ip = client_address[0]

            if is_denied(client_ip):
                print(f"Connection not allowed from {client_ip}:{client_address[1]}")
                response = "Blocked"
                client_socket.send(response.encode('utf-8'))
                client_socket.close()
                logging.info(f"BLOCKED - Connection from {client_ip}:{client_address[1]}")

            elif is_allow(client_ip):
                # Forward traffic through NAT
                NAT_Gate(client_socket, client_address, server_ip, server_port)
                logging.info(f"ALLOWED - Connection from {client_ip}:{client_address[1]}")

            else:
                print(f"Connection from unknown IP {client_ip}:{client_address[1]}")
                response = "Server Said Unknown Client"
                client_socket.send(response.encode('utf-8'))
                client_socket.close()
                logging.info(f"UNKNOWN - Connection from {client_ip}:{client_address[1]}")

        except Exception as e:
            print(f"An error occurred: {e}")
            logging.error(f"An error occurred: {e}")

        finally:
            server_socket.close()

if __name__ == "__main__":
    # Setup Socket Server
    server_ip = '127.0.0.2'
    server_port = 8081
    allowed_ip = ["127.0.0.1", "192.168.11.147", "192.168.11.167"]
    denied_ip = [""]  # You might want to add IP addresses to deny in this list
    gateway_ip = '127.0.0.2'  # ip for address translation
    main()
