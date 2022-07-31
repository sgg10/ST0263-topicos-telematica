import os
import logging
from socket import socket
from socket import AF_INET, SOCK_STREAM, SOL_SOCKET, SO_REUSEADDR

from jinja2 import Template

from minetypes import MINETYPES

MAX_CONNECTIONS = 1000
PORT = 80

logging.basicConfig(level=logging.INFO, format='%(levelname)s | %(message)s')


def create_server(port):
    _server = socket(AF_INET, SOCK_STREAM)
    _server.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    _server.bind(("0.0.0.0", port))
    _server.listen(MAX_CONNECTIONS)
    return _server

def generate_header(ext):
    header = "HTTP/0.9 200 OK\n"
    content_type = MINETYPES.get(ext, "text/html")
    header += f"Content-Type: {content_type}\n\n"
    return header


def generate_response(resource, ext):
    _file = f'./files/{"index.html" if resource == "" else resource}'

    if resource == "":
        with open(_file, "r") as f:
            template = Template(f.read())
            data = {"files": os.listdir("./files")}
            result = template.render(**data)
            return result

    mode = "r" if ext == "txt" else "rb"
    with open(_file, mode) as f:
        return f.read()


def run_server(_server: socket):
    while True:
        connection, _ = _server.accept()
        try:
            request = connection.recv(1024)
            info = request.decode("utf-8").split()
            resource = info[1].lstrip("/")
            logging.info(f"REQUEST: {' | '.join(info[:2])}")
            ext = "txt" if resource == "" else resource.split(".")[-1]

            try:
                header = generate_header(ext).encode("utf-8")
                body = generate_response(resource, ext)
                response = header + body.encode("utf-8") if ext == "txt" else body
            except Exception as e:
                logging.error(str(e))
                header = "HTTP/0.9 404 Not Found\n\n"
                response = header.encode("utf-8")+ '<html><body><h1>Error 404: file not found</h1></body></html>'.encode("utf-8")

            logging.info(f"RESPONSE: {header.decode('utf-8')}")

            connection.send(response)
            connection.close()
        except:
            pass

def main():
    _server = create_server(PORT)
    print(f"Server listen at http://localhost:{PORT}/")
    run_server(_server)

if __name__ == '__main__':
    main()