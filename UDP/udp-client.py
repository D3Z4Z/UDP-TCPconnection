import socket

SERVER_IP = "192.168.1.81"
SERVER_PORT = 12000
BUFFER_SIZE = 1024
TIMEOUT_SECONDS = 5


def create_client_socket():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.settimeout(TIMEOUT_SECONDS)
    return sock


def send_and_receive(sock, message):
    sock.sendto(message.encode(), (SERVER_IP, SERVER_PORT))
    data, _server_address = sock.recvfrom(BUFFER_SIZE)
    return data.decode()


def chat_loop(sock):
    print(f"UDP client talking to {SERVER_IP}:{SERVER_PORT}. Type 'quit' to exit.")
    while True:
        message = input("\nClient: ")
        if not message:
            continue
        if message.lower() == "quit":
            print("Conversation ended.")
            break

        try:
            reply = send_and_receive(sock, message)
            print(f"Server: {reply}")
        except socket.timeout:
            print(f"No response after {TIMEOUT_SECONDS} seconds. The server may be down or the packet was lost.")
        except ConnectionResetError:
            print("The server is not reachable (ICMP port unreachable).")


def main():
    client_socket = create_client_socket()
    try:
        chat_loop(client_socket)
    except (KeyboardInterrupt, EOFError):
        print("\nCancelled by user.")
    except OSError as error:
        print(f"Socket error: {error}")
    finally:
        client_socket.close()
        print("Client socket closed.")


if __name__ == "__main__":
    main()