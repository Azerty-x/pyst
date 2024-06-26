from app.app import Server, render
from http.server import HTTPServer

hostName = "localhost"
port = 8080

# Your first route
@Server.route("/")
def cast(handler):
    render(handler)


if __name__ == "__main__":
    serv = HTTPServer(("localhost", 8080), Server)
    print(f"Server : http://{hostName}:{port}")
    try:
        serv.serve_forever()
    except KeyboardInterrupt:
        pass
    serv.server_close()
    