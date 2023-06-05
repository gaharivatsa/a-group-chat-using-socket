import socket
import threading

# Server configuration
SERVER_HOST = '127.0.0.1'
SERVER_PORT = 5000

# Create a socket object
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to a specific address and port
server_socket.bind((SERVER_HOST, SERVER_PORT))

# Listen for incoming connections
server_socket.listen(2)
print('Server listening on {}:{}'.format(SERVER_HOST, SERVER_PORT))

clients = []
clients_lock = threading.Lock()  # Lock to ensure thread-safe modification of clients list


def handle_client(client_socket, client_address):
    while True:
        # Receive data from the client
        data = client_socket.recv(1024).decode('utf-8')

        if data == "exit":
            # Client has disconnected
            print('{}:{} disconnected'.format(client_address[0], client_address[1]))

            with clients_lock:
                clients.remove(client_socket)

            break

        # Print the received message
        print('Received from {}: {}'.format(client_address, data))

        # Broadcast the message to other clients
        with clients_lock:
            for client in clients:
                if client != client_socket:
                    message = '{}:{} {}'.format(client_address[0], client_address[1], data)
                    client.send(message.encode('utf-8'))

    # Check if all clients are disconnected
    with clients_lock:
        if len(clients) == 0:
            print("All clients disconnected. Server shutting down.")
            server_socket.close()
            


# Accept incoming connections
while True:
    client_socket, client_address = server_socket.accept()
    print('New connection from {}:{}'.format(client_address[0], client_address[1]))

    with clients_lock:
        clients.append(client_socket)

    # Create a new thread to handle the client
    client_thread = threading.Thread(target=handle_client, args=(client_socket, client_address))
    client_thread.start()
