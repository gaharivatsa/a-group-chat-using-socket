import socket
import threading

# Server configuration
SERVER_HOST = '127.0.0.1'
SERVER_PORT = 5000

# Create a socket object
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect to the server
client_socket.connect((SERVER_HOST, SERVER_PORT))

# Function to handle receiving messages from the server
def receive_messages():
    while True:
        # Receive data from the server
        print(" ")
        data = client_socket.recv(1024).decode('utf-8')

        if not data:
            # Server has disconnected
            print('Server disconnected')
            break

        # Print the received message
        print('\n',{data})

# Start a separate thread to receive messages from the server
receive_thread = threading.Thread(target=receive_messages)
receive_thread.start()

# Main loop to send messages to the server
while True:
    message = input('Enter a message: ')
    print("  ")
    # Send the message to the server
    client_socket.send(message.encode('utf-8'))

    if message.lower() == 'exit':
        # Exit the loop and close the socket
        break

# Close the socket
client_socket.close()
