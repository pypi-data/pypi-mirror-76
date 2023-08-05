"""Functional tests for zope.app.catalog


"""
import doctest
import unittest
import re

from zope.testing import renormalizing

from .testing import PatchedAppCatalogLayer

from zope.app.wsgi.testlayer import http as _http


def http(query_str, *args, **kwargs):
    wsgi_app = PatchedAppCatalogLayer.make_wsgi_app()
    # Strip leading \n
    query_str = query_str.lstrip()
    kwargs.setdefault('handle_errors', False)
    if not isinstance(query_str, bytes):
        query_str = query_str.encode("utf-8")
    return _http(wsgi_app, query_str, *args, **kwargs)



def test_suite():
    checker = renormalizing.RENormalizing((
        (re.compile("HTTP/1.0"), "HTTP/1.1"),
        (re.compile(r"u('[^']*')"), r"\1"),
    ))

    suite = doctest.DocFileSuite(
        'regression.rst',
        globs={
            'http': http,
            'getRootFolder': PatchedAppCatalogLayer.getRootFolder,
        },
        checker=checker,
        optionflags=(doctest.ELLIPSIS
                     | doctest.NORMALIZE_WHITESPACE
                     | renormalizing.IGNORE_EXCEPTION_MODULE_IN_PYTHON2),
    )
    suite.layer = PatchedAppCatalogLayer
    return suite
