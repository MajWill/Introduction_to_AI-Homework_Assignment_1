import socket
import json
from vacuum_2d import (
    BidimensionalVacuumAgent,
    rooms,
)  # Import necessary functions/classes from your existing script


def start_server():
    # Initialize socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Bind the socket to a specific address and port
    host = "localhost"
    port = 12345
    server_socket.bind((host, port))

    # Listen for incoming connections (max 1 client)
    server_socket.listen(1)

    print(f"Listening for incoming connections on {host}:{port}")

    # Accept a connection from Unity
    client_socket, address = server_socket.accept()
    print(f"Connection established with {address}")

    try:
        # Initialize your vacuum simulation
        random_matrix = rooms(10, 10)
        vacuum = BidimensionalVacuumAgent(random_matrix)
        vacuum.vacuum_drop()
        room_history, agent_history = vacuum.movement(450)

        # For demonstration, we're sending the last state
        data_to_send = {
            "room_state": room_history[-1].tolist(),
            "vacuum_pos": agent_history[-1],
        }

        # Serialize data to JSON format
        json_data = json.dumps(data_to_send)

        # Send data to Unity
        client_socket.sendall(json_data.encode("utf-8"))

    finally:
        # Close the socket
        client_socket.close()


# Start the server
if __name__ == "__main__":
    start_server()
