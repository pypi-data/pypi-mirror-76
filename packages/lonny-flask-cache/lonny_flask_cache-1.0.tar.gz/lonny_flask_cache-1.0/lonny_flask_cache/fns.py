from flask import make_response
from datetime import timedelta

CACHE_CONTROL_HEADER = "Cache-Control"
DEFAULT_CACHE_BEHAVIOUR = "no-cache"
DEFAULT_CACHE_HOURS = 24

def cache(age = timedelta(hours = DEFAULT_CACHE_HOURS)):
    seconds = int(age.total_seconds())
    def wrapper(fn):
        def wrapped(*args, **kwargs):
            resp = make_response(fn(*args, **kwargs))
            resp.headers[CACHE_CONTROL_HEADER] = f"max-age={seconds}"
            return resp
        return wrapped
    return wrapper