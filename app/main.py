# Uncomment this to pass the first stage
import socket


def main():
    # You can use print statements as follows for debugging, they'll be visible when running tests.
    print("Logs from your program will appear here!")

    # Uncomment this to pass the first stage
    #
    # server_socket = socket.create_server(("localhost", 4221), reuse_port=True)
    # server_socket.accept() # wait for client
    
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind(("localhost", 4221))
        server_socket.listen()
        conn, addr = server_socket.accept()
        with conn:
            print('Connected by', addr)
            while True:
                data = conn.recv(1024)
                print(data)
                if not data:
                    break
                conn.sendall(b"HTTP/1.1 200 OK\r\n\r\n")

if __name__ == "__main__":
    main()
