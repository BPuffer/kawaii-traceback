# circular import
import another2

another2.hello()

def hello():
    print(f"Hello, world! (module: {__name__})")