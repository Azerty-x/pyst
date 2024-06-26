from http.server import BaseHTTPRequestHandler
from jinja2 import Template


class Server(BaseHTTPRequestHandler):
    routes = {}
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        path = self.path.split("?")[0]
        if path in self.routes:
            self.routes[path](self)
        else:
            self.wfile.write(bytes("""<html>
<head>
    <title>Page not found</title>
</head>
<body>
    <h1>Error 404</h1>
</body>
</html>""", "utf-8"))

    

    @classmethod
    def route(cls, endpoint=None, methods=None, **options):
        def decorator(func):
            cls.routes[endpoint] = func
            print(cls.routes)
            return func
        return decorator

def get_args(handler):
    args = {}
    args_brut = handler.path.split("?")[1]
    args_dev = args_brut.split("&")
    for arg in args_dev:
        tmp_arg = arg.split("=")
        args[tmp_arg[0]] = tmp_arg[1]
    return args

def render(handler, path="/", **options):
    args = options
    try:
        with open(f"./src{path}/index.html") as f:
            template = Template(f.read())
            p = handler.path.split("?")
            if len(p)>1:
                args_brut = p[1].split("&")
                for arg in args_brut:
                    tmp_arg = arg.split("=")
                    args[tmp_arg[0]] = tmp_arg[1]
                handler.wfile.write(bytes(template.render(**args), "utf-8"))
            else:
                handler.wfile.write(bytes(template.render(), "utf-8"))
    except FileNotFoundError:
        handler.wfile.write(bytes("""<html>
<head>
    <title>Page not found</title>
</head>
<body>
    <h1>Error 404</h1>
</body>
</html>""", "utf-8"))
