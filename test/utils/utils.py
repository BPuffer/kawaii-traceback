import pytest
import kawaiitb
from kawaiitb import kraceback
from kawaiitb import KTBException

__CONFIG__ = {
    "translate_keys": {
        "__test__": {
            "extend": "zh_hans"
        }
    },
    "default_lang": "__test__"
}

@pytest.fixture(scope="class")
def kawaii_tb_config():
    kawaiitb.load_config(__CONFIG__)
    yield
    kawaiitb.unload()

class KTBTestBase:
    console_output = False

    def __init_subclass__(cls, console_output=False, **kwargs):
        super().__init_subclass__(**kwargs)
        cls.console_output = console_output

    def try_print_exc(self, e):
        if self.console_output:
            print("".join(kraceback.format_exception(e)))

    def pack_exc(self, HandlerType, exc):
        ktb = KTBException.from_exception(exc)
        handler = HandlerType(type(exc), exc, exc.__traceback__)
        assert handler.can_handle(ktb)
        messages = list(handler.handle(ktb))
        return ktb, handler, messages, "".join(messages)

def raise_error(ExceptionType=Exception, msg="test"):
    raise ExceptionType(msg)
