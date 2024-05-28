# Uncomment this to pass the first stage
import socket
import threading
import re
import sys


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
                
def create_server_refactored(host,port):
    #TODO: need to learn how is this happening using regular expression. Also, change this code to align.
    with socket.create_server((host, port)) as socket_server:
        conn,addr = socket_server.accept()
        print(f"accepted connection from the {addr}")
        
        data = conn.recv(1024).decode()
        try:
            match = re.match(r"GET\s+(/echo/)?(\S+)\s+HTTP/1\.1", data)
            if match:
                filtered_data = match.group(2)
                response = f"HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nContent-Length: {len(filtered_data)}\r\n\r\n{filtered_data}"
            else:
                raise IndexError
        except IndexError:
            response = "HTTP/1.1 404 Not Found\r\n\r\n"
        conn.sendall(response.encode())
                        
def create_server_codecrafter(host, port):
    with socket.create_server((host, port)) as socket_server:
        while True:
            connection,address = socket_server.accept()
            print(f"accepted connection from the {address}")
            #client_connection(connection)
            connection_thread=threading.Thread(target=client_connection,args=(connection,))
            connection_thread.start()

def read_directory_data(filtered_data):
    directory = sys.argv[2]
    file_path = f"{directory}{filtered_data}"
    # read the file contents from the directory
    try:
        with open(file_path,"r") as f:
            data = f.read()
    except FileNotFoundError:
        data = None
    return data

def write_to_file(file_name,contents):
    # the idea is to read the data from the post request and write it to a file.
    directory = sys.argv[2]
    file_path = f"{directory}{file_name}"
    print(file_path)
    try:
        with open(file_path,"w") as f:
            f.write(contents)
    except Exception as e:
        raise IndexError


def get_http_process(filtered_data,request_data):
    content_type= "text/plain"
    if filtered_data == '/user-agent':
        filtered_data=request_data[2].split(" ")[1]
    elif filtered_data.startswith('/files'):
        filtered_data=filtered_data.split("/files/")[1]
        filtered_data = read_directory_data(filtered_data)
        content_type = "application/octet-stream"
        if filtered_data is None:
            raise IndexError
    else:
        filtered_data=filtered_data.split("/echo/")[1]
    response = f"HTTP/1.1 200 OK\r\nContent-Type: {content_type}\r\nContent-Length: {len(filtered_data)}\r\n\r\n{filtered_data}"
    return response
    

def client_connection(conn):
    data = conn.recv(1024).decode()
    print("data is",data)
    try:
        request_data = data.split("\r\n")
        filtered_data = request_data[0].split(" ")[1]
        content_type = "text/plain"
        http_verb = request_data[0].split(" ")[0]
        print("http_verb is: ",http_verb)
        if http_verb =='GET':
            if filtered_data !='/':
                response = get_http_process(filtered_data,request_data)
            else:
                response = f"HTTP/1.1 200 OK\r\nContent-Type: {content_type}\r\nContent-Length: {len(filtered_data)}\r\n\r\n{filtered_data}"
        elif http_verb == "POST":
            # read the data from the server post request
            if filtered_data.startswith('/files'):
                filename = filtered_data.split("/files/")[1]
                print(filename)
                body = data.split("\r\n")[-1]
                print("body is:",body)
                #how to get the content body from the curl request
                write_to_file(filename,body)
                
            response = f"HTTP/1.1 201 Created\r\n\r\n"
        print(filtered_data)
        #TODO: what is a better way to read the header from the text?
        
    except IndexError:
        response = "HTTP/1.1 404 Not Found\r\n\r\n"
    print(response)
    conn.sendall(response.encode())
    conn.close()


def main():
    # You can use print statements as follows for debugging, they'll be visible when running tests.
    print("Logs from your program will appear here!")
    HOST = "localhost"
    PORT = 4221
    # Uncomment this to pass the first stage
    #
    # server_socket = socket.create_server(("localhost", 4221), reuse_port=True)
    # server_socket.accept() # wait for client
    #create_server_refactored(HOST,PORT)
    create_server_codecrafter(HOST,PORT)

if __name__ == "__main__":
    main()