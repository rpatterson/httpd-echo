#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""A Simple Python HTTP server that echos the request in the response."""

import argparse
import email.message
import socket
from email.generator import BytesGenerator
from http.cookies import SimpleCookie
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib import parse

__version__ = '0.3.1'

__all__ = ["EchoHTTPRequestHandler"]


class EchoHTTPRequestHandler(BaseHTTPRequestHandler):
    """A Simple Python HTTP server that echos the request in the response."""

    def do_GET(self):  # noqa:N802, pylint: disable=invalid-name
        """Echo a request without a body."""
        message = self.get_message()
        self.send_head()
        BytesGenerator(self.wfile).flatten(message, unixfrom=False)

    do_HEAD = do_GET  # noqa:N815

    do_OPTIONS = do_GET  # noqa:N815

    do_DELETE = do_GET  # noqa:N815

    def do_POST(self):  # noqa:N802, pylint: disable=invalid-name
        """Echo a request with a body."""
        message = self.get_message()
        try:
            length = int(self.headers["Content-Length"])
        except (TypeError, ValueError) as exc:
            message.set_payload(f"Invalid Content-Length: {exc}")
        else:
            message.set_payload(self.rfile.read(length))
        finally:
            self.send_head()
            BytesGenerator(self.wfile).flatten(message, unixfrom=False)

    do_PUT = do_POST  # noqa:N815

    do_PATCH = do_POST  # noqa:N815

    def send_head(self):
        """Send all the basic, required headers."""
        self.send_response(200)
        # self.send_header("Content-Type", "text/rfc822-headers; charset=UTF-8")
        self.send_header("Content-Type", "text/plain; charset=UTF-8")
        self.send_header("Last-Modified", self.date_time_string())
        self.end_headers()

    def get_message(self):
        """Assemble the basic message including query parameters."""
        message = email.message.Message()
        message["Method"] = self.command
        message["Path"] = self.path

        server_url = parse.SplitResult(scheme="http", netloc=f"{self.server.server_name}:{self.server.server_port}",
                                       path="", query="", fragment="")
        request_url = parse.urlsplit(server_url.geturl() + self.path)
        for name, value in parse.parse_qs(request_url.query).items():
            message.add_header(name, value[0])

        cookies = SimpleCookie(self.headers.get('Cookie'))
        for name, value in cookies.items():
            message.add_header(f'Cookie-{name}', repr(value))

        return message


def main(args=None, default_port=8000):
    """Run the echo HTTP server."""
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument(
        "--address", "-a", default="127.0.0.1",
        help="Hostname or IP address to accept requests on.")
    parser.add_argument(
        "--port", "-p", type=int,
        help="Port number to accept requests on. If not specified, use the first available port after 8000.")

    args = parser.parse_args(args)

    if args.port is None:
        args.port = default_port
        bound = False
        while not bound:
            try:
                httpd = HTTPServer((args.address, args.port), EchoHTTPRequestHandler)
            except socket.error as exc:
                args.port += 1
                if args.port > 65535:
                    raise ValueError("No available port found") from exc
            else:
                bound = True
    else:
        httpd = HTTPServer((args.address, args.port), EchoHTTPRequestHandler)

    print(f"Echoing HTTP at http://{args.address}:{args.port}, press Ctrl+C to stop.")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print(" - Stopped")


if __name__ == "__main__":
    main()
