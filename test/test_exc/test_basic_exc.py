from test.utils import KTBTestCase

class TestExceptionFormatting(KTBTestCase, preview=True):

    def test_StopIteration(self):
        """kawaiitb.handlers.defaults.StopIterationHandler"""
        from kawaiitb.handlers.defaults import StopIterationHandler

        def gen():
            for i in range(10):
                yield i

        obj = type("_Foo", (), {"g": gen()})()

        try:
            while True:
                # 非常复杂的ast解析定位测试
                # 要解析的是'instance.g'这个表达式
                _ = str((f"{next(obj. \
                                 g):0<10}".join([]), "str")[0]).strip()
        except StopIteration as e:
            self.try_preview(e)
            ktb, handler, msgs, tb = self.pack_exc(StopIterationHandler, e)
            assert "'obj.g'" in tb

        try:
            while True:
                # 这次是obj.g.__next__()
                _ = str((f"{obj. \
                                 g. \
                    __next__():0<10}".join([]), "str")[0]).strip()
        except StopIteration as e:
            self.try_preview(e)
            ktb, handler, msgs, tb = self.pack_exc(StopIterationHandler, e)
            assert "'obj.g'" in tb

    def test_StopAsyncIteration(self):
        """kawaiitb.handlers.defaults.StopAsyncIterationHandler"""
        from kawaiitb.handlers.defaults import StopAsyncIterationHandler
        import asyncio

        async def async_gen():
            for i in range(10):
                yield i

        async def run_test():
            abj = type("_Aoo", (), {"g": async_gen()})()
            try:
                while True:
                    # 很复杂的异步ast解析定位测试
                    # 要解析的是'obj.g'这个表达式
                    _ = str((f"{await anext(abj. \
                              g):0<10}".join([]), "str")[0]).strip()
            except StopAsyncIteration as e:
                self.try_preview(e)
                ktb, handler, msgs, tb = self.pack_exc(StopAsyncIterationHandler, e)
                assert "'abj.g'" in tb

            abj = type("_Aoo", (), {"g": async_gen()})()
            try:
                while True:
                    # 这次是abj.g.__anext__()
                    _ = str((f"{await abj. \
                              g. \
                    __anext__():0<10}".join([]), "str")[0]).strip()
            except StopAsyncIteration as e:
                self.try_preview(e)
                ktb, handler, msgs, tb = self.pack_exc(StopAsyncIterationHandler, e)
                assert "'abj.g'" in tb

        # 使用辅助函数运行异步测试
        asyncio.run(run_test())

    def test_overflow(self):
        """OverflowError异常"""
        from kawaiitb.handlers.defaults import OverflowErrorHandler
        try:
            import math
            a = math.exp(1000)
        except OverflowError as e:
            self.try_preview(e)
            ktb, handler, msgs, tb = self.pack_exc(OverflowErrorHandler, e)
            # assert "math.exp" in tb



