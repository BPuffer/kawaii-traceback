__all__ = ["entry"]

def entry(confirm):
    if confirm == "I'm sure I wan't to raise a ImportError":
        from test.utils.__imperr_partinit_attr import func_b
        return func_b(confirm)
