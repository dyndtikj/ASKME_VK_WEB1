from django.test import TestCase
HELLO_WORLD = b"Hello world!\n"

#  gunicorn --workers=2 tests:application

def simple_app(environ, start_response):
    status = '200 OK'
    print(environ)
    response_headers = [('Content-type', 'text/plain')]
    start_response(status, response_headers)
    return [HELLO_WORLD]


application = simple_app


class AppClass:
    def __init__(self, environ, start_response):
        self.environ = environ
        self.start = start_response

    def __iter__(self):
        status = '200 OK'
        response_headers = [('Content-type', 'text/plain')]
        self.start(status, response_headers)
        yield HELLO_WORLD
