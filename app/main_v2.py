# Implement this code using SOLID principles
from abc import ABC, abstractmethod
from enum import Enum
import socket
import threading
import sys

# first layout the structure of the code.


class NoDataException(Exception):
    pass


class ContentTypeHeaders(Enum):
    TextPlain = "text/plain"
    HTML = "text/html"
    JSON = "application/json"
    FILE = "application/octet-stream"


class HTTPStatusCode(Enum):
    OK = 200
    CREATED = 201
    BAD_REQUEST = 400
    NOT_FOUND = 404


class HTTPVerb(Enum):
    GET = "GET"
    POST = "POST"


class Headers(ABC):
    # if constructor can be created in a Headers
    @abstractmethod
    def statusline(self):
        pass

    @abstractmethod
    def headers(self):
        pass

    @abstractmethod
    def response_body(self):
        pass


class RequestHeaderImpl(Headers):
    def __init__(self, request_header: str) -> None:
        super().__init__()
        self.request_line = request_header
        self.header = None
        self.request_body = None

    def statusline(self):
        self.http_method = self.request_line
        self.request_target = self.request_line
        self.http_version = self.request_line
        # add CRLF to end of the request

    def headers(self):
        self.host_port = self.header
        self.user_agent = self.header
        self.media_type = (
            self.header
        )  # specifies the media type that the client can accept.
        # CRLF is the end of the header.

    def request_body(self):
        return self.body


class ResponseHeaderImpl(Headers):
    # make it a builder class
    # we can build response header from a request header class.
    def __init__(self) -> None:
        # self.header = requestbody.headers()
        pass

    # don't forget to add CRLF to end of the response.
    # convert the class object to a string


class HTTPRequest:
    # takes input as a request obj and returns a response object
    def create_http_request(self, request: str) -> RequestHeaderImpl:
        # takes input as a request str and returns a request header
        pass

    def create_server(self, host, port):
        with socket.create_server((host, port)) as socket_server:
            conn, addr = socket_server.accept()
            print(f"Connected to: {addr}")
            # i think I am confused on how to create multiple connections
            # conn -> threaded function
            thread = threading.Thread(target=create_multiple_connections, args=(conn))
            thread.start()

    def create_multiple_connections(self,conn):
        while True:
            data = conn.recv(1024)
            if not data:
                raise NoDataException

            request_header = RequestHeaderImpl(data)
            request_target = request_header.request_line.request_target
            match request_header.request_line.http_method:
                case HTTPVerb.GET :

                    useragent_key = request_header.headers.user_agent
                    useragent_value = request_header.headers.user_agent
                    if request_target == '/': #write down different cases of the request target
                        response_body = HTTPStatusCode.OK

                        # status_code = 200 OK

                    elif request_target == "/index.html":
                        response_body = HTTPStatusCode.NOT_FOUND

                    elif request_target.startswith("/echo/"):
                        response_body = HTTPStatusCode.OK
                        content_type = ContentTypeHeaders.TextPlain
                        # create a response object

                        if request_header.headers.accept_encoding == "gzip":
                            new_header = "Content-Encoding: gzip"

                        elif request_header.headers.accept_encoding == "invalid-encoding":

                    elif request_target.startswith("/files/"):
                        filepath = ""
                        response_body = HTTPStatusCode.OK
                        body = self.read_file(filepath)
                        content_type = ContentTypeHeaders.FILE
                        response_body += str(content_length)+ content_type+ useragent_value + body

                    if useragent == '/user-agent':
                        response_body = HTTPStatusCode.OK
                        content_type = ContentTypeHeaders.TextPlain
                        content_length = len(useragent_value)

                        response_body += str(content_length)+ content_type+useragent_value

                case HTTPVerb.POST :
                    if request_target.startswith("/files/"):
                        filepath = ""
                        response_body = HTTPStatusCode.CREATED
                        body = self.read_file(filepath)
                        content_type = ContentTypeHeaders.FILE
                        response_body += str(content_length)+ content_type+ useragent_value + body

            conn.sendall(data)

    def read_compressed_data(self):
        # reads compressed data from a http request
        pass

    def read_file(self, filepath):
        filename = sys.argv[2]
        try:
            with open(filename, "rb") as f:
                return f.read()
        except FileNotFoundError:
            raise Exception

    def write_to_file(self, filepath, file_contents):
        try:
            with open(filepath, "w") as w:
                w.write(file_contents)
        except FileNotFoundError:
            raise Exception
