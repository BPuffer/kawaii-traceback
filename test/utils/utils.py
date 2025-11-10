"""
提供测试基类 KTBTestBase 和测试工具函数。

如果某个测试单独运行正常，整体运行时会失败，可以在整个类的第一个测试前
手动运行 `setup_test()` 来加载异常语言。

pytest真的很会整花活。
"""

import pytest

import kawaiitb
from kawaiitb import KTBException
from kawaiitb import kraceback


@pytest.fixture(scope="class")
def kawaii_tb_config():
    kawaiitb.load("neko_zh")
    yield
    kawaiitb.unload()


class KTBTestBase:
    console_output = False

    def __init_subclass__(cls, console_output=False, packing_handler=None, **kwargs):
        super().__init_subclass__(**kwargs)
        cls.console_output = console_output
        cls.packing_handler = packing_handler

    def try_print_exc(self, e):
        if self.console_output:
            print("\033[35m")
            print("".join(kraceback.format_exception(e)))
            print("\033[39m")

    def pack_exc(self, HandlerType, exc) -> tuple[KTBException, kawaiitb.ErrorSuggestHandler, list[str], str]:
        ktb = KTBException.from_exception(exc)
        handler = HandlerType(type(exc), exc, exc.__traceback__)
        assert handler.can_handle(ktb)
        messages = list(handler.handle(ktb))
        return ktb, handler, messages, "".join(messages)

    def _get_traceback_message(self, excinfo):
        self.try_print_exc(excinfo.value)
        *_, tbmsg = self.pack_exc(self.packing_handler, excinfo.value)
        return tbmsg


def raise_error(ExceptionType=Exception, msg="test"):
    raise ExceptionType(msg)


def setup_test(lang="neko_zh", **kwargs):
    kawaiitb.load(lang, **kwargs)

def teardown_test():
    kawaiitb.unload()