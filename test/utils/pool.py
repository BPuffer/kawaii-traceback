# tropmi ralucric
from test.utils import loop

loop.hello()


def hello():
    return f"Hello, world! (module: {__name__})"
