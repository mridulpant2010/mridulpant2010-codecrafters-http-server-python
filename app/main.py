# Uncomment this to pass the first stage
import socket


def create_server(host, port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as socket_server:
        socket_server.bind((host, port))
        socket_server.listen()
        conn, addr = socket_server.accept()
        with conn:
            print(f"Connected by {addr}")
            while True:
                data = conn.recv(1024)
                print(data)
                if not data:
                    break
                conn.sendall(b"HTTP/1.1 200 OK\r\n\r\n")
                
def create_server_codecrafter(host, port):
    with socket.create_server((host, port),reuse_port=True) as socket_server:
        connection,address = socket_server.accept()
        print(f"accepted connection from the {address}")
        
        data = connection.recv(1024)
        print(data)
        connection.sendall(b"HTTP/1.1 200 OK\r\n\r\n")
        
        
        

def main():
    # You can use print statements as follows for debugging, they'll be visible when running tests.
    print("Logs from your program will appear here!")
    HOST = "localhost"
    PORT = 4221
    # Uncomment this to pass the first stage
    #
    # server_socket = socket.create_server(("localhost", 4221), reuse_port=True)
    # server_socket.accept() # wait for client
    create_server_codecrafter(HOST,PORT)

if __name__ == "__main__":
    main()
