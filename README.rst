==========
httpd-echo
==========
A Simple Python HTTP server that echos the request in the response
------------------------------------------------------------------

Provide a simple HTTP server that tries to echo the request back in the
response in the most sensible way possible.  This can be useful for, testing,
debugging, stubbing out a local server in systems that have a hard-coded
assumption of making HTTP requests, etc.::

  $ python -m httpdecho
  Echoing HTTP at http://localhost:8000 ...

Examples
--------

Without specifying a port, the server will try to find the next available port
starting at 8000 to try and be as predictable as possible::

  >>> import sys
  >>> import time
  >>> import subprocess
  >>> from six.moves import SimpleHTTPServer
  >>> startup_delay = 0.5
  >>> simple_popen = subprocess.Popen(
  ...     [sys.executable, '-m', SimpleHTTPServer.__name__]
  ...     ); time.sleep(1)
  >>> echo_popen = subprocess.Popen(
  ...     [sys.executable, '-m', 'httpdecho']
  ...     ); time.sleep(1)
  >>> echo_popen.poll()
  >>> simple_popen.kill()

Once running, HTTP requests are echoed in the responses.  The default response
body format is basically HTTP header format, from
``http.client.HTTPMessage``::

  >>> import io
  >>> import requests
  >>> import email
  >>> get_response = requests.delete('http://localhost:8001')
  >>> get_body = email.message_from_string(get_response.text)
  >>> print(get_body['Method'])
  DELETE
  >>> print(get_body['Path'])
  /
  >>> print(get_body.get_payload())
  <BLANKLINE>

Query parameters are also included::

  >>> query_response = requests.get(
  ...     'http://localhost:8001', params=dict(Foo='foo'))
  >>> query_body = email.message_from_string(query_response.text)
  >>> print(query_body['Foo'])
  foo

If the request is a ``POST`` or another method that accepts a body on the
request, the body or the responses body will contain the POST body::

  >>> post_response = requests.patch(
  ...     'http://localhost:8001', data=dict(Bar='bar'))
  >>> post_body = email.message_from_string(post_response.text)
  >>> print(post_body.get_payload())
  Bar=bar

Shutdown the server::

  >>> echo_popen.kill()
