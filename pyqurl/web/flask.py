import functools
from flask import request

from pyqurl.core import create_query_from_dict

def use_query_filters(*, offset=None, limit=None):
    def wrapper(fn):
        @functools.wraps(fn)
        def wrapped(*args, **kwargs):
            args_ = {**request.args}

            if offset and "offset" not in request.args:
                args_["offset"] = offset

            if limit and "limit" not in request.args:
                args_["limit"] = limit

            query = create_query_from_dict(args_)
            return fn(*args, **kwargs, query=query)
        return wrapped
    return wrapper
