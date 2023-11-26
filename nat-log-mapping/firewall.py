import socket
import logging  
from datetime import datetime
import secrets

BLOCK_IPS = ['192.168.11.110', '192.168.11.111']

# NAT mapping: Public IP and Port to Private IP and Port
NAT_MAPPING = {
    ('127.0.0.2', 9090): ('192.168.0.1', 8080),
    ('127.0.0.2', 8080): ('192.168.0.2', 7070),
    ('127.0.0.2', 7070): ('192.168.0.3', 7070),
    #('public_ip', public_port): ('private_ip', private_port)
}

logging.basicConfig(filename='firewall_log.txt', level=logging.INFO, format='%(asctime)s - %(message)s')

# NAT Firewall function
def nat_firewall(client_rec, public_ip, public_port):
    if client_rec in BLOCK_IPS:
        return None, None
    private_ip, private_port = NAT_MAPPING.get((public_ip, public_port), (None, None))
    return private_ip, private_port

DATA_LOG_FILE = 'data_log.txt'

# Log encrypted client data
def log_encrypted_data(client_ip, encrypted_data, key):
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    log_entry = f"{timestamp} Client IP: {client_ip} - {encrypted_data} | {key}\n"
    with open(DATA_LOG_FILE, 'a') as log_file:
        log_file.write(log_entry)

# Generate a random key
def generate_random_key():
    return secrets.token_bytes(32)

# Encrypt data using XOR
def encrypt_data(data, key):
    encrypted_data = bytes([a ^ b for a, b in zip(data.encode(), key)])
    return encrypted_data

# Authenticate user function
def authenticate_user(auth_message):
    # Parse the authentication message
    _, username, password = auth_message.split(':')

    # For simplicity, this example assumes a hard-coded username and password
    valid_username = "user"
    valid_password = "password"

    return username == valid_username and password == valid_password

# Main function
def main():
    # Create a socket object
    firewall_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Bind the socket
    firewall_port = 9090
    firewall_socket.bind(('127.0.0.2', firewall_port))

    # Listen for incoming connections
    firewall_socket.listen(5)

    print(f"Firewall is running and listening on port {firewall_port}...")

    while True:
        try:
            # Accept a new connection
            client_socket, client_address = firewall_socket.accept()

            # Receive client IP, server IP, and server port
            client_ip, server_ip, server_port = client_socket.recv(1024).decode().strip().split(':')
            print(f"Connection from {client_ip}")

            print(f"Received Client IP: {client_ip}, Server IP: {server_ip}, Server Port: {server_port}")

            # Check if the connection is allowed by the NAT firewall
            private_ip, private_port = nat_firewall(client_ip, server_ip, int(server_port))
            if private_ip and private_port:
                print(f"Mapping to Private IP: {private_ip}, Port: {private_port}")
                client_socket.send(f"Connected to {server_ip}:{server_port}".encode())

                # User Login
                auth_message = client_socket.recv(1024).decode()
                if authenticate_user(auth_message):
                    _, username, _ = auth_message.split(':')
                    print(f"User {username} authenticated successfully.")

                    try:
                        # Generate a random key for encryption
                        encryption_key = generate_random_key()

                        while True:
                            data = client_socket.recv(1024).decode()
                            if not data:
                                print(f"Client from {client_ip} has disconnected.")
                                break

                            print(f"Received data from client: {data}")

                            # Encrypt the data with the generated key
                            encrypted_data = encrypt_data(data, encryption_key)
                            
                            # Log the encrypted data along with the key
                            log_encrypted_data(client_ip, encrypted_data.hex(), encryption_key.hex())

                            if data.upper() == 'Q':
                                print(f"Client from {client_ip} has requested to disconnect.")
                                break

                    except Exception as e:
                        print(f"An error occurred: {e}")

                    finally:
                        client_socket.close()
                        print(f"Connection with {client_ip} closed.")

                    # Log the allowed connection
                    logging.info(f"ALLOWED - {client_ip} connected to {server_ip}:{server_port} mapped to {private_ip}:{private_port}")

                else:
                    print(f"Authentication failed for user {username}. Connection closed.")
                    client_socket.send("Authentication failed. Connection closed.".encode())
                    client_socket.close()

            else:
                print("Connection blocked by NAT firewall.")
                client_socket.send("Connection blocked by NAT firewall.".encode())
                client_socket.close()
                print(f"Connection with {client_ip} closed.")
                # Log the blocked connection
                logging.info(f"BLOCKED - {client_ip}")

        except Exception as e:
            print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
