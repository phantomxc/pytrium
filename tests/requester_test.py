import sys
# Clear possible previous mock... there has to be better way
sys.modules.pop('atrium.requester', '')

from mock import MagicMock
requestsMock = sys.modules['requests'] = MagicMock(spec=[
    'get',
    'post',
    'put',
    'delete',
    'exceptions'
])

from atrium.requester import request
from atrium.errors import (
    NetworkError,
    RequestTimeoutError
)

import pytest
import unittest
import json

class HTTPError(Exception):
    pass

class CustomConnectionError(Exception):
    pass

class ProxyError(Exception):
    pass

class SSLError(Exception):
    pass

class Timeout(Exception):
    pass

# Create the fake exceptions in our mock
requestsMock.exceptions.return_value = MagicMock()
requestsMock.exceptions.HTTPError = HTTPError
requestsMock.exceptions.ConnectionError = CustomConnectionError
requestsMock.exceptions.ProxyError = ProxyError
requestsMock.exceptions.SSLError = SSLError
requestsMock.exceptions.Timeout = Timeout


class TestRequest(unittest.TestCase):

    def setUp(self):
        self.headers = {
            "foo": "bar"
        }
        self.payload = {
            "bar": "baz"
        }

    def testGet(self):
        requestsMock.get.side_effect = None
        request("foo", "GET", headers=self.headers)
        requestsMock.get.assert_called_with("foo", headers=self.headers)

    def testPost(self):
        request(
            "foo",
            "POST",
            headers=self.headers,
            payload=self.payload
        )
        requestsMock.post.assert_called_with(
            "foo",
            headers=self.headers,
            data=json.dumps(self.payload)
        )

    def testPut(self):
        request(
            "foo",
            "PUT",
            headers=self.headers,
            payload=self.payload
        )
        requestsMock.put.assert_called_with(
            "foo",
            headers=self.headers,
            data=json.dumps(self.payload)
        )

    def testDelete(self):
        request("foo", "DELETE", headers=self.headers)
        requestsMock.delete.assert_called_with("foo", headers=self.headers)

    def testHttpError(self):
        requestsMock.get.side_effect = HTTPError('foo')

        with pytest.raises(NetworkError):
            request("foo", "GET")

    def testConnectionError(self):
        requestsMock.get.side_effect = CustomConnectionError('foo')

        with pytest.raises(NetworkError):
            request("foo", "GET")

    def testProxyError(self):
        requestsMock.get.side_effect = ProxyError('foo')

        with pytest.raises(NetworkError):
            request("foo", "GET")

    def testSslErrorP(self):
        requestsMock.get.side_effect = SSLError('foo')

        with pytest.raises(NetworkError):
            request("foo", "GET")

    def testTimeout(self):
        requestsMock.get.side_effect = Timeout('foo')

        with pytest.raises(RequestTimeoutError):
            request("foo", "GET")
