# circular import
from . import pool

pool.hello()

def hello():
    print(f"Hello, world! (module: {__name__})")