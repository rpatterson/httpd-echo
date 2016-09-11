"""
A Simple Python HTTP server that echos the request in the response.
"""

import socket
import argparse
from six.moves.urllib import parse
import email.message
try:
    from email.generator import BytesGenerator
except ImportError:
    # BBB Python 2 compatibility
    from email.generator import Generator as BytesGenerator

from six.moves import BaseHTTPServer

parser = argparse.ArgumentParser(
    description=__doc__,
    formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument(
    '--address', '-a', default='localhost',
    help='Hostname or IP address to accept requests on.')
parser.add_argument(
    '--port', '-p', help='Port to accept requests on.  '
    'If not specified, use the first available port after 8000.')


class EchoHTTPRequestHandler(BaseHTTPServer.BaseHTTPRequestHandler):
    """
    A Simple Python HTTP server that echos the request in the response.
    """

    def do_GET(self):
        """
        Echo a request without a body.
        """
        message = self.get_message()
        self.send_head()
        BytesGenerator(self.wfile).flatten(message, unixfrom=False)

    do_HEAD = do_GET
    do_OPTIONS = do_GET
    do_DELETE = do_GET

    def do_POST(self):
        """
        Echo a request with a body.
        """
        message = self.get_message()
        message.set_payload(self.rfile.read(
            int(self.headers['Content-Length'])))
        self.send_head()
        BytesGenerator(self.wfile).flatten(message, unixfrom=False)

    do_PUT = do_POST
    do_PATCH = do_POST

    def send_head(self):
        """
        Send all the basic, required headers.
        """
        self.send_response(200)
        self.send_header("Content-Type", 'text/rfc822-headers')
        self.send_header("Last-Modified", self.date_time_string())
        self.end_headers()

    def get_message(self):
        """
        Assemble the basic message including query parameters.
        """
        message = email.message.Message()
        message['Method'] = self.command
        message['Path'] = self.path

        server_url = parse.SplitResult('http', '{0}:{1}'.format(
            self.server.server_name, self.server.server_port), '', '', '')
        request_url = parse.urlsplit(server_url.geturl() + self.path)
        for header, value in parse.parse_qs(request_url.query).items():
            message.add_header(header, value[0])

        return message


def main(args=None, default_port=8000):
    """
    Run the echo HTTP server.
    """
    args = parser.parse_args(args)

    port = args.port
    if port is None:
        port = default_port
        bound = False
        while not bound:
            try:
                httpd = BaseHTTPServer.HTTPServer(
                    (args.address, port), EchoHTTPRequestHandler)
            except socket.error:
                port += 1
                if port > 65535:
                    raise ValueError('No available port found')
            else:
                bound = True
    else:
        httpd = BaseHTTPServer.HTTPServer(
            (args.address, int(port)), EchoHTTPRequestHandler)

    print('Echoing HTTP at http://{0}:{1} ...'.format(args.address, port))
    httpd.serve_forever()


if __name__ == '__main__':
    main()
