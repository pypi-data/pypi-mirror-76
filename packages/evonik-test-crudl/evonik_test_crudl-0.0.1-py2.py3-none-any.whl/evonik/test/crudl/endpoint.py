import pytest


class Endpoint:
    """Specification of endpoints of an API.

    The following endpoints with specific meaning can be specified:

    1. create, signature: create(spec)
    2. read, signature:      get(data)
    2. update, signature: update(data, spec)
    3. delete, signature: delete(data)
    5. list, signature:     list(limit, offset)
    """

    def __init__(self, endpoint,
                 dummy=None):
        self.endpoint = endpoint
        self.dummy = dummy

    def call(self, *args, **kwargs):
        return self.endpoint(*args, **kwargs)


class Endpoints:
    def __init__(self, **endpoints):
        for k, v in endpoints.items():
            setattr(self, k, v)
