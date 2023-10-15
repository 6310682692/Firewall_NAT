import socket
import logging

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
def nat_firewall(client_rec,public_ip, public_port):
    if client_rec in BLOCK_IPS:
        return None, None
    private_ip, private_port = NAT_MAPPING.get((public_ip, public_port), (None, None))
    return private_ip, private_port

# Main function
def main():
    # Create a socket object
    firewall_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Bind the socket
    firewall_socket.bind(('127.0.0.2', 9090))

    # Listen for incoming connections
    firewall_socket.listen(5)
    print("Firewall is running and listening on port 9090...")

    while True:
        # Accept a new connection
        client_socket, client_address = firewall_socket.accept()

         # Receive client IP, server IP, and server port
        client_ip, server_ip, server_port = client_socket.recv(1024).decode().strip().split(':')
        print(f"Connection from {client_ip}")

        print(f"Received Client IP: {client_ip}, Server IP: {server_ip}, Server Port: {server_port}")

        # Check if the connection is allowed by the NAT firewall
        private_ip, private_port = nat_firewall(client_ip,server_ip, int(server_port))
        if private_ip and private_port:
            print(f"Mapping to Private IP: {private_ip}, Port: {private_port}")
            client_socket.send(f"Connected to {server_ip}:{server_port}".encode())

            try:
                while True:
                    data = client_socket.recv(1024).decode()
                    if not data:
                        print(f"Client from {client_ip} has disconnected.")
                        break

                    print(f"Received data from client: {data}")
                    if data.upper() == 'Q':
                        print(f"Client from {client_ip} has disconnected.")
                        break

            except Exception as e:
                print(f"An error occurred: {e}")

            finally:
                client_socket.close()

            # Log the allowed connection
            logging.info(f"ALLOWED - {client_ip} connected to {server_ip}:{server_port} mapped to {private_ip}:{private_port}")

        else:
            print("Connection blocked by NAT firewall.")
            client_socket.send("Connection blocked by NAT firewall.".encode())
            client_socket.close()
            # Log the blocked connection
            logging.info(f"BLOCKED - {client_ip}")

if __name__ == "__main__":
    main()
