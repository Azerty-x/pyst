from app.app import Server
from http.server import HTTPServer

hostName = "localhost"
port = 8080


if __name__ == "__main__":
    serv = HTTPServer(("localhost", 8080), Server)
    print(f"Server : http://{hostName}:{port}")
    try:
        serv.serve_forever()
    except KeyboardInterrupt:
        pass
    serv.server_close()
    