import json
import requests

from .errors import NetworkError, RequestTimeoutError


def request(url, method, headers={}, payload={}, options={}):
    try:
        if method == "GET":
            r = requests.get(url, headers=headers)
        elif method == "POST":
            r = requests.post(url, headers=headers, data=json.dumps(payload))
        elif method == "PUT":
            r = requests.put(url, headers=headers, data=json.dumps(payload))
        elif method == "DELETE":
            r = requests.delete(url, headers=headers)
        return r

    except requests.exceptions.HTTPError as e:
        raise NetworkError(repr(e))

    except requests.exceptions.ConnectionError as e:
        raise NetworkError(repr(e))

    except requests.exceptions.ProxyError as e:
        raise NetworkError(repr(e))

    except requests.exceptions.SSLError as e:
        raise NetworkError(repr(e))

    except requests.exceptions.Timeout as e:
        raise RequestTimeoutError(repr(e))
