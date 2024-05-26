# Uncomment this to pass the first stage
import socket
from urllib import request


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
                # how to get this request target from the server?
                # how to identify if it is a valid request-line or the invalid request-line?
                # invalid request line with 400 error or a 301
                response = b"HTTP/1.1 200 OK\r\n\r\n"
                # ['GET / HTTP/1.1', 'Host: localhost:4221', '', '']
                req = data.decode().split("\r\n")
                if not data:
                    break
                
                if req[0].split("/")!="/":
                    response = b"HTTP/1.1 404 Not Found\r\n\r\n"
                conn.sendall(response)
                
def create_server_codecrafter(host, port):
    with socket.create_server((host, port)) as socket_server:
        connection,address = socket_server.accept()
        print(f"accepted connection from the {address}")
        
        data = connection.recv(1024)
        print(data)
        response = b"HTTP/1.1 200 OK\r\n\r\n"
        
        request_data=data.decode().split("\r\n")
        print(request_data)
        if request_data[0].split(" ")[1]!="/":
            response = b"HTTP/1.1 404 Not Found\r\n\r\n"
        
        connection.sendall(response)
        
        

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
