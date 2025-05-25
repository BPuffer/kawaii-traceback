import pytest
from ..utils.utils import KTBTestBase
from kawaiitb.handlers.defaults import StopAsyncIterationHandler


async def async_gen():
    for i in range(10):
        yield i


async def async_gen_infinite():
    while True:
        yield 666


class TestStopAsyncIteration(KTBTestBase, console_output=False):
    @pytest.mark.asyncio
    async def test_anext_builtin(self):
        """测试使用内置anext()函数引发的StopAsyncIteration"""
        obj = type("_Foo", (), {"g": async_gen(), "h": async_gen()})()
        confuser1 = async_gen_infinite()
        confuser2 = async_gen_infinite()
        confuser3 = async_gen_infinite()
        with pytest.raises(StopAsyncIteration) as excinfo:
            while True:
                await anext(confuser1)
                _ = str((f"{await anext(confuser2)}{await anext(obj.g):0<{await anext(confuser3)}}".join([]), "str")[0]).strip()
        e = excinfo.value
        ktb, handler, msgs, tbmsg = self.pack_exc(StopAsyncIterationHandler, e)
        self.try_print_exc(e)
        assert "'obj.g'" in tbmsg
        assert "confuser" not in tbmsg

    @pytest.mark.asyncio
    async def test_anext_method(self):
        """测试使用__anext__()方法引发的StopAsyncIteration"""
        obj = type("_Foo", (), {"g": async_gen(), "h": async_gen()})()
        confuser1 = async_gen_infinite()
        confuser2 = async_gen_infinite()
        confuser3 = async_gen_infinite()
        with pytest.raises(StopAsyncIteration) as excinfo:
            while True:
                await anext(confuser1)
                _ = str((f"{await anext(confuser2)}{await obj.h.__anext__():0<{await anext(confuser3)}}".join([]), "str")[0]).strip()
        e = excinfo.value
        ktb, handler, msgs, tbmsg = self.pack_exc(StopAsyncIterationHandler, e)
        self.try_print_exc(e)
        assert "'obj.h'" in tbmsg
        assert "confuser" not in tbmsg
