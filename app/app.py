from http.server import BaseHTTPRequestHandler
from jinja2 import Template


class Server(BaseHTTPRequestHandler):
    routes = {}
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        print(self.path)
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


def render(handler, path="/", **options):
    try:
        with open(f"./src{path}/index.html") as f:
            template = Template(f.read())
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
