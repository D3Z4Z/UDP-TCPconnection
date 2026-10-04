import socket

SERVER_IP = "0.0.0.0"
SERVER_PORT = 12000
BUFFER_SIZE = 1024


def create_server_socket():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((SERVER_IP, SERVER_PORT))
    return sock


def build_reply(message):
    return message


def run_server(sock):
    print(f"UDP server is running on port {SERVER_PORT}. Press Ctrl+C to stop.")
    while True:
        try:
            data, client_address = sock.recvfrom(BUFFER_SIZE)
            message = data.decode()
            print(f"Got message from {client_address}: {message}")

            reply = build_reply(message)
            sock.sendto(reply.encode(), client_address)
            print(f"Replied to {client_address}: {reply}")
        except UnicodeDecodeError:
            print("Received data that was not valid text, ignoring it.")
        except ConnectionResetError:
            pass
        except OSError as error:
            print(f"Socket error while handling a packet: {error}")


def main():
    server_socket = None
    try:
        server_socket = create_server_socket()
        run_server(server_socket)
    except OSError as error:
        print(f"Could not start the server: {error}")
    except KeyboardInterrupt:
        print("\nServer stopped by user.")
    finally:
        if server_socket:
            server_socket.close()
            print("Server socket closed.")


if __name__ == "__main__":
    main()