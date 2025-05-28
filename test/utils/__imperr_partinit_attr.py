__all__ = ["func_b"]

def func_b(confirm):
    if confirm == "I'm sure I wan't to raise a ImportError":
        from test.utils.imperr_partinit_attr import entry
        return entry(confirm)
