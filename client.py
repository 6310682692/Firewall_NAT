import socket

def main():
    # Setup client to connect to server
    server_ip = '127.0.0.2'
    server_port = 8081

    # Create a socket object for the client
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        # Connect to the server
        client_socket.connect((server_ip, server_port))
        print(f"Connected to {server_ip}:{server_port}")

        while True:
            # test sending data
            message = input("You can now sent message to the server: ")
            client_socket.send(message.encode('utf-8'))
            # Check User status
            if message.upper() == "Q":
                break

        # test response
        data = client_socket.recv(1024)
        print(f"Received data from server: {data.decode('utf-8')}")

    except Exception as e:
        print(f"An error occurred: {e}")

    finally:
        client_socket.close()

if __name__ == "__main__":
    main()
