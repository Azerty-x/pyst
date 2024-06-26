from http.server import BaseHTTPRequestHandler, HTTPServer
from jinja2 import Template

# hostName = "localhost"
# port = 8080

class Server(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        print(self.path)
        if "." in self.path:
            pass
        elif "?" in self.path:
            args = {}
            path = self.path.split("?")
            arg = path[1]
            a = arg.split("&")
            for elt in a:
                elt_sp = elt.split("=")
                args[elt_sp[0]] = elt_sp[1]
            print(args)
            with open(f"./src{path[0]}/index.html") as f:
                template = Template(f.read())
                self.wfile.write(bytes(template.render(**args), "utf-8"))

        elif self.path != "/":
            with open(f"./src{self.path}/index.html") as f:
                template = Template(f.read())
                self.wfile.write(bytes(template.render(), "utf-8"))
        else:
            with open(f"./src/index.html") as f:
                template = Template(f.read())
                self.wfile.write(bytes(template.render(), "utf-8"))
        


# if __name__ == "__main__":
#     serv = HTTPServer((hostName, port), Server)
#     print(f"Server : http://{hostName}:{port}")
#     try:
#         serv.serve_forever()
#     except KeyboardInterrupt:
#         pass

#     serv.server_close()
#     print("stopped")