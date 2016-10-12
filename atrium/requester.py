import json
import requests

from atrium.errors import NetworkError, RequestTimeoutError

def request(url, method, headers={}, payload={}, options={}):
    try:
        if method == "GET":
            return requests.get(url, headers=headers)
        elif method == "POST":
            return requests.post(url, headers=headers, data=json.dumps(payload))
        elif method == "PUT":
            return requests.put(url, headers=headers, data=json.dumps(payload))
        elif method == "DELETE":
            return requests.delete(url, headers=headers)

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
