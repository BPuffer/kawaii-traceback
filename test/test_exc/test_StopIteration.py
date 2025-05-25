import pytest
from test.utils.utils import KTBTestBase
from kawaiitb.handlers.defaults import StopIterationHandler


def gen():
    for i in range(10):
        yield i


def gen2():
    while True:
        yield 666


class TestStopIteration(KTBTestBase, console_output=False):
    def test_next_builtin(self):
        obj = type("_Foo", (), {"g": gen(), "h": gen()})()
        confuser1 = gen2()
        confuser2 = gen2()
        confuser3 = gen2()
        with pytest.raises(StopIteration) as excinfo:
            while True:
                next(confuser1)
                _ = str((f"{next(confuser2)}{next(obj.g):0<{next(confuser3)}}".join([]), "str")[0]).strip()
        e = excinfo.value
        ktb, handler, msgs, tbmsg = self.pack_exc(StopIterationHandler, e)
        self.try_print_exc(e)
        assert "'obj.g'" in tbmsg
        assert "confuser" not in tbmsg

    def test_next_method(self):
        obj = type("_Foo", (), {"g": gen(), "h": gen()})()
        confuser1 = gen2()
        confuser2 = gen2()
        confuser3 = gen2()
        with pytest.raises(StopIteration) as excinfo:
            while True:
                next(confuser1)
                _ = str((f"{next(confuser2)}{obj.h.__next__():0<{next(confuser3)}}".join([]), "str")[0]).strip()
        e = excinfo.value
        ktb, handler, msgs, tbmsg = self.pack_exc(StopIterationHandler, e)
        self.try_print_exc(e)
        assert "'obj.h'" in tbmsg
        assert "confuser" not in tbmsg
