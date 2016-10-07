
def cleanData(key):

    def wrapper(func):

        def anotherWrapper(*args, **kwargs):
            if kwargs.get('payload'):
                # Wrap our payload with the key provided
                new_data = {}
                new_data[key] = kwargs.get('payload')
                kwargs['payload'] = new_data
            # Unpack using the same key
            res = func(*args, **kwargs)[key]

            # storigify them
            if isinstance(res, list):
                return [storage(r) for r in res]
            return storage(res)

        return anotherWrapper

    return wrapper


class Storage(dict):
    """
    A Storage object is like a dictionary except `obj.foo` can be used
    in addition to `obj['foo']`.

        >>> o = storage(a=1)
        >>> o.a
        1
        >>> o['a']
        1
        >>> o.a = 2
        >>> o['a']
        2
        >>> del o.a
        >>> o.a
        Traceback (most recent call last):
            ...
        AttributeError: 'a'

    """
    def __getattr__(self, key):
        try:
            return self[key]
        except KeyError as k:
            raise AttributeError(k)

    def __setattr__(self, key, value):
        self[key] = value

    def __delattr__(self, key):
        try:
            del self[key]
        except KeyError as k:
            raise AttributeError(k)

    def __repr__(self):
        return '<Storage ' + dict.__repr__(self) + '>'

storage = Storage
