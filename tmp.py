try:
    a = 1
    b = 0 - 0
    c = (a + a) / (a - a)
except ZeroDivisionError as e:
    import traceback
    print("".join(traceback.format_exception(e)))

    # code from here
    # id=
