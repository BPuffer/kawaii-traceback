import pytest

from test.utils.utils import KTBTestBase


class TestNameError(KTBTestBase, console_output=False):
    @pytest.mark.skip(reason="NameError TODO")
    def test_spelling_error_print(self):
        """测试拼写错误的print"""
        prant("awa")  # noqa

    @pytest.mark.skip(reason="NameError TODO")
    def test_spelling_error_numpy(self):
        """测试拼写错误的库中方法"""
        # TODO: 产生的是AttributeError，而不是NameError，挪过去
        import typing
        T = typing.TypoVar("T")  # noqa

    @pytest.mark.skip(reason="NameError TODO")
    def test_missing_import(self):
        """测试忘记导入模块"""
        asyncio.run(asyncio.sleep(1))  # noqa

    @pytest.mark.skip(reason="NameError TODO")
    def test_nameerror_var_in_self(self_test, lang):
        class Foo:
            def __init__(self):
                self.attr = 1
            def bar(self):
                return f"{attr}"  # noqa
        with pytest.raises(AttributeError) as excinfo:
            foo = Foo()
            foo.bar()
        tbmsg = self_test._get_traceback_message(excinfo)
        assert "self.attr" in tbmsg