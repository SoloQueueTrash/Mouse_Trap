import socket

def messageHandler(message):
    response = "tasssss bem"
    return response

# Define the IP address and port to use
IP_ADDRESS = 'localhost'
PORT = 12345

# Create a socket object
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to a specific IP address and port
server_socket.bind((IP_ADDRESS, PORT))

# Listen for incoming connections
server_socket.listen()

print(f"Server listening on {IP_ADDRESS}:{PORT}")

while(1):
    # Wait for a client to connect
    client_socket, client_address = server_socket.accept()

    print(f"Client connected from {client_address[0]}:{client_address[1]}")

    # Receive data from the client
    data = client_socket.recv(1024)

    print(f"Received data from client: {data.decode()}")

    # Send data back to the client
    response = messageHandler(data.decode())
    
    if(response == "exit"):
        response = "Closing socket ..."

        # Close the client socket
        client_socket.close()

        # Close the server socket
        server_socket.close()

        client_socket.send(response.encode())
        break

    client_socket.send(response.encode())