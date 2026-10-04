import socket
import threading

SERVER_IP = "0.0.0.0"
SERVER_PORT = 12001
BUFFER_SIZE = 1024
BACKLOG = 5


def create_listening_socket():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind((SERVER_IP, SERVER_PORT))
    sock.listen(BACKLOG)
    return sock


def receive_loop(connection, stop_event):
    while not stop_event.is_set():
        try:
            data = connection.recv(BUFFER_SIZE)
        except socket.timeout:
            continue
        except OSError:
            break

        if not data:
            print("\nClient disconnected. Press Enter to wait for a new client.")
            break

        message = data.decode(errors="replace")
        if message.lower() == "quit":
            print("\nClient ended the conversation. Press Enter to wait for a new client.")
            break

        print(f"\nClient: {message}\nServer: ", end="", flush=True)
    stop_event.set()


def send_loop(connection, stop_event):
    while not stop_event.is_set():
        try:
            message = input("Server: ")
        except EOFError:
            message = "quit"
        if stop_event.is_set():
            break
        if not message:
            continue
        try:
            connection.sendall(message.encode())
        except OSError:
            print("Could not send, the client is gone.")
            break
        if message.lower() == "quit":
            print("Conversation ended.")
            break
    stop_event.set()


def handle_client(connection, client_address):
    connection.settimeout(1)
    stop_event = threading.Event()
    receiver = threading.Thread(target=receive_loop, args=(connection, stop_event), daemon=True)
    receiver.start()
    try:
        send_loop(connection, stop_event)
    finally:
        stop_event.set()
        receiver.join(timeout=2)
        connection.close()
        print("Connection closed.\n")


def run_server(listener):
    print(f"TCP chat server waiting for a client on port {SERVER_PORT}. Press Ctrl+C to stop.")
    while True:
        connection, client_address = listener.accept()
        print(f"Connected to {client_address}. Type 'quit' to end the chat.")
        handle_client(connection, client_address)


def main():
    listener = None
    try:
        listener = create_listening_socket()
        run_server(listener)
    except OSError as error:
        print(f"Could not start the server: {error}")
    except KeyboardInterrupt:
        print("\nServer stopped by user.")
    finally:
        if listener:
            listener.close()
            print("Listening socket closed.")


if __name__ == "__main__":
    main()