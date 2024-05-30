# Uncomment this to pass the first stage
import socket
import threading
import sys
import gzip


def create_server_codecrafter(host, port):
    with socket.create_server((host, port)) as socket_server:
        while True:
            connection, address = socket_server.accept()
            print(f"accepted connection from the {address}")
            # client_connection(connection)
            connection_thread = threading.Thread(
                target=client_connection, args=(connection,)
            )
            connection_thread.start()


def read_directory_data(filtered_data):
    directory = sys.argv[2]
    file_path = f"{directory}{filtered_data}"
    # read the file contents from the directory
    try:
        with open(file_path, "r") as f:
            data = f.read()
    except FileNotFoundError:
        data = None
    return data


def write_to_file(file_name, contents):
    # the idea is to read the data from the post request and write it to a file.
    directory = sys.argv[2]
    file_path = f"{directory}{file_name}"
    print(file_path)
    try:
        with open(file_path, "w") as f:
            f.write(contents)
    except FileNotFoundError as e:
        raise IndexError


def validate_encoding(filtered_data, request_data):
    accept_encoding = request_data[2].split(" ")
    print("accept encoding", accept_encoding)
    # print(type(accept_encoding))
    if "gzip" in accept_encoding or "gzip," in accept_encoding:
        print("gzip ")
        compress_filtered_data = gzip.compress(filtered_data.encode("utf-8"))
        response = (
            f"HTTP/1.1 200 OK\r\nContent-Encoding: gzip\r\nContent-Type: text/plain\r\nContent-Length: {len(compress_filtered_data)}\r\n\r\n".encode()
            + compress_filtered_data
        )
        print("compressed data ", compress_filtered_data)
        # uncompressed_data = bytes.fromhex(hex_data)
        # decompressed_data = gzip.decompress(compress_filtered_data)
        # print("decompressed data ",decompressed_data.decode())
    else:
        response = f"HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nContent-Length: {len(filtered_data)}\r\n\r\n{filtered_data}".encode()
    print(response)
    return response


def get_http_process(filtered_data, request_data):
    content_type = "text/plain"
    if filtered_data == "/user-agent":
        filtered_data = request_data[2].split(" ")[1]
    elif filtered_data.startswith("/files"):
        filtered_data = filtered_data.split("/files/")[1]
        filtered_data = read_directory_data(filtered_data)
        content_type = "application/octet-stream"
        if filtered_data is None:
            raise IndexError
    elif filtered_data.startswith("/echo"):
        filtered_data = filtered_data.split("/echo/")[1]
        # fetch the accept_encoding value
        response = validate_encoding(filtered_data, request_data)
        print("response is ", response)
        return response
    else:
        raise IndexError

    response = f"HTTP/1.1 200 OK\r\nContent-Type: {content_type}\r\nContent-Length: {len(filtered_data)}\r\n\r\n{filtered_data}".encode()
    return response


def client_connection(conn):
    data = conn.recv(
        1024
    ).decode()  # TODO: how can i convert this data to a hashmap? is it even possible?
    print("data is", data)
    try:
        request_data = data.split("\r\n")
        filtered_data = request_data[0].split(" ")[1]
        http_verb = request_data[0].split(" ")[0]
        print("http_verb is: ", http_verb)
        if http_verb == "GET":
            content_type = "text/plain"
            if filtered_data != "/":
                response = get_http_process(filtered_data, request_data)
            else:
                response = f"HTTP/1.1 200 OK\r\nContent-Type: {content_type}\r\nContent-Length: {len(filtered_data)}\r\n\r\n{filtered_data}".encode()
        elif http_verb == "POST":
            # read the data from the server post request
            if filtered_data.startswith("/files"):
                filename = filtered_data.split("/files/")[1]
                print(filename)
                body = data.split("\r\n")[-1]
                print("body is:", body)
                # how to get the content body from the curl request
                write_to_file(filename, body)
            response = f"HTTP/1.1 201 Created\r\n\r\n".encode()
        print(filtered_data)
        # TODO: what is a better way to read the header from the text?
    except IndexError:
        response = "HTTP/1.1 404 Not Found\r\n\r\n".encode()
    print(response)
    conn.sendall(response)
    conn.close()


def main():
    print("Logs from your program will appear here!")
    HOST = "localhost"
    PORT = 4221
    create_server_codecrafter(HOST, PORT)


if __name__ == "__main__":
    main()
