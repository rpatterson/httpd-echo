#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
A Simple Python HTTP server that echos the request in the response.
"""

import socket
import email.message
from six.moves.urllib import parse
try:
    from email.generator import BytesGenerator
except ImportError:
    # BBB Python 2 compatibility
    from email.generator import Generator as BytesGenerator
from six.moves import BaseHTTPServer


__all__ = ['EchoHTTPRequestHandler']


class EchoHTTPRequestHandler(BaseHTTPServer.BaseHTTPRequestHandler):
    """
    A Simple Python HTTP server that echos the request in the response.
    """

    def do_GET(self):  # noqa:N802, pylint: disable=invalid-name
        """
        Echo a request without a body.
        """
        message = self.get_message()
        self.send_head()
        BytesGenerator(self.wfile).flatten(message, unixfrom=False)

    do_HEAD = do_GET     # noqa:N815
    do_OPTIONS = do_GET  # noqa:N815
    do_DELETE = do_GET   # noqa:N815

    def do_POST(self):  # noqa:N802, pylint: disable=invalid-name
        """
        Echo a request with a body.
        """
        message = self.get_message()
        try:
            length = int(self.headers['Content-Length'])
        except (TypeError, ValueError) as exc:
            message.set_payload("Invalid Content-Length: " + str(exc))
        else:
            message.set_payload(self.rfile.read(length))
        finally:
            self.send_head()
            BytesGenerator(self.wfile).flatten(message, unixfrom=False)

    do_PUT = do_POST    # noqa:N815
    do_PATCH = do_POST  # noqa:N815

    def send_head(self):
        """
        Send all the basic, required headers.
        """
        self.send_response(200)
        self.send_header("Content-Type", 'text/rfc822-headers; charset=UTF-8')
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
    import argparse  # pylint: disable=import-outside-toplevel
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument(
        '--address', '-a', default='localhost',
        help='Hostname or IP address to accept requests on.')
    parser.add_argument(
        '--port', '-p', help='Port to accept requests on.  '
        'If not specified, use the first available port after 8000.')

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
                    # Silence pylint to keep it python2 compatible.
                    raise ValueError('No available port found')  # pylint: disable=raise-missing-from
            else:
                bound = True
    else:
        httpd = BaseHTTPServer.HTTPServer(
            (args.address, int(port)), EchoHTTPRequestHandler)

    print('Echoing HTTP at http://{0}:{1} ...'.format(args.address, port))
    httpd.serve_forever()


if __name__ == '__main__':
    main()
