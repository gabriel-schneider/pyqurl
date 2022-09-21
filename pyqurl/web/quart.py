import functools
from quart import request

from pyqurl.core import create_query_from_args

def use_query_filters():
    def wrapper(fn):
        @functools.wraps(fn)
        def wrapped(*args, **kwargs):        
            query = create_query_from_args(request.args)    
            return fn(*args, **kwargs, query=query)
        return wrapped
    return wrapper