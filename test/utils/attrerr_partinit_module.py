def entry(confirm):
    if confirm == "I'm sure I wan't to raise an AttributeError":
        from test.utils import __attrerr_partinit_module_2nd
        __attrerr_partinit_module_2nd.hello()

def hello():
    return f"Hello, world! (module: {__name__})"