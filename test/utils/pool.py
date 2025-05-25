from . import loop

loop.hello()

def hello():
    print(f"Hello, world! (module: {__name__})")