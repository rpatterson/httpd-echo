"""
Test the echo HTTP server.
"""

import doctest

from six.moves import SimpleHTTPServer  # noqa


def load_tests(loader=None, tests=None, ignore=None):
    return doctest.DocFileSuite(
        'README.rst', optionflags=doctest.REPORT_NDIFF)
