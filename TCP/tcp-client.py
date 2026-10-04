import socket
import threading

SERVER_IP = "192.168.1.81"
SERVER_PORT = 12001
BUFFER_SIZE = 1024
CONNECT_TIMEOUT = 10


def create_client_socket():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(CONNECT_TIMEOUT)
    return sock


def receive_loop(sock, stop_event):
    while not stop_event.is_set():
        try:
            data = sock.recv(BUFFER_SIZE)
        except socket.timeout:
            continue
        except OSError:
            break

        if not data:
            print("\nServer disconnected. Press Enter to exit.")
            break

        message = data.decode(errors="replace")
        if message.lower() == "quit":
            print("\nServer ended the conversation. Press Enter to exit.")
            break

        print(f"\nServer: {message}\nClient: ", end="", flush=True)
    stop_event.set()


def send_loop(sock, stop_event):
    while not stop_event.is_set():
        try:
            message = input("Client: ")
        except EOFError:
            message = "quit"
        if stop_event.is_set():
            break
        if not message:
            continue
        try:
            sock.sendall(message.encode())
        except OSError:
            print("Could not send, the server is gone.")
            break
        if message.lower() == "quit":
            print("Conversation ended.")
            break
    stop_event.set()


def chat(sock):
    sock.settimeout(1)
    stop_event = threading.Event()
    receiver = threading.Thread(target=receive_loop, args=(sock, stop_event), daemon=True)
    receiver.start()
    try:
        send_loop(sock, stop_event)
    finally:
        stop_event.set()
        receiver.join(timeout=2)


def main():
    client_socket = create_client_socket()
    try:
        print(f"Connecting to {SERVER_IP}:{SERVER_PORT}...")
        client_socket.connect((SERVER_IP, SERVER_PORT))
        print("Connected to TCP server. Type 'quit' to exit.")
        chat(client_socket)
    except ConnectionRefusedError:
        print("Connection refused. Make sure the TCP server is running.")
    except socket.timeout:
        print("The connection attempt timed out.")
    except (ConnectionResetError, BrokenPipeError):
        print("The server closed the connection unexpectedly.")
    except KeyboardInterrupt:
        print("\nCancelled by user.")
    except OSError as error:
        print(f"Socket error: {error}")
    finally:
        client_socket.close()
        print("TCP socket closed.")


if __name__ == "__main__":
    main()