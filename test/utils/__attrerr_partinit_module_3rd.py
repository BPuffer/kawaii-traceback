from test.utils import attrerr_partinit_module
attrerr_partinit_module.hello()

def hello():
    return f"Hello, world! (module: {__name__})"
