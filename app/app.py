from http.server import BaseHTTPRequestHandler, HTTPServer
from jinja2 import Template


class Server(BaseHTTPRequestHandler):
    routes = {}

    def do_GET(self):
        if (".png" in self.path) or (".jpeg" in self.path) or (".ico" in self.path):
            self.send_response(200)
            self.send_header("Content-type", "image/*")
            self.end_headers()
            self.wfile.write(load_binary(self.path))
        else:
            path = self.path.split("?")[0]
            if path in self.routes:
                self.routes[path](self)
            else:
                self.send_error(404,"Page not found")
                self.end_headers()
    

    def do_POST(self):
        path = self.path.split("?")[0]
        if path in self.routes:
            self.routes[path](self)
        else:
            self.send_error(404, "Page not found")
            self.end_headers()

    def redirect(self, path):
        self.send_response(302)
        self.send_header('Location', path)
        self.end_headers()
    

    @classmethod
    def route(cls, endpoint=None, methods=None, **options):
        def decorator(func):
            cls.routes[endpoint] = func
            print(cls.routes)
            return func
        return decorator

    def run(port):
        serv = HTTPServer(("localhost", port), Server)
        print(f"Server started at : http://localhost:{port}")
        try:
            serv.serve_forever()
        except KeyboardInterrupt:
            pass
        serv.server_close()

def get_args(handler):
    args = {}
    args_brut = handler.path.split("?")[1]
    args_dev = args_brut.split("&")
    for arg in args_dev:
        tmp_arg = arg.split("=")
        args[tmp_arg[0]] = tmp_arg[1]
    return args

def get_body(handler):
    content_len = int(handler.headers.get('Content-Length'))
    post_body = handler.rfile.read(content_len)
    args = {}
    tmp_args = post_body.decode("UTF-8").split("&")
    for arg in tmp_args:
        tmp_arg = arg.split("=")
        args[tmp_arg[0]] = tmp_arg[1]
    return args

def load_binary(filename):
    with open(f".{filename}", "rb") as f:
        return f.read()

def render(handler, path="/", **options):
    args = options
    try:
        with open(f"./src{path}/index.html") as f:
            handler.send_response(200)
            handler.send_header("Content-type", "text/html")
            handler.end_headers()
            template = Template(f.read())
            p = handler.path.split("?")
            if args:
                if len(p)>1:
                    args_brut = p[1].split("&")
                    for arg in args_brut:
                        tmp_arg = arg.split("=")
                        args[tmp_arg[0]] = tmp_arg[1]
                handler.wfile.write(bytes(template.render(**args), "utf-8"))
            else:
                handler.wfile.write(bytes(template.render(), "utf-8"))
    except FileNotFoundError:
        handler.send_error(404, "HTML Page not found.")
        handler.end_headers()