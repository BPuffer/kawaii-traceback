# circular import
from test.utils import pool

pool.hello()


def hello():
    return f"Hello, world! (module: {__name__})"
