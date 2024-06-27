from app.app import Server, render
from http.server import HTTPServer

hostName = "localhost"
port = 8080

# Your first route
@Server.route("/")
def cast(handler):
    render(handler)


if __name__ == "__main__":
    Server.run(8080)