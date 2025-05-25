import pytest

from test.utils.utils import KTBTestBase


class TestNameError(KTBTestBase, console_output=True):
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
