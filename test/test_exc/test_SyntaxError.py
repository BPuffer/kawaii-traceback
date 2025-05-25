import pytest

from ..utils.utils import KTBTestBase

class TestSyntaxError(KTBTestBase, console_output=False):

    @pytest.mark.skip(reason="SyntaxError TODO")
    def test_syntax_error_invalid_lex(self):
        """测试语法错误 - 无效词法"""
        exec("what can i say?")

    @pytest.mark.skip(reason="SyntaxError TODO")
    def test_syntax_error_unexpected_end(self):
        """测试语法错误 - 不预期结束"""
        exec("1 + 2 *")

    @pytest.mark.skip(reason="SyntaxError TODO")
    def test_syntax_error_invalid_indent(self):
        """测试语法错误 - 无效缩进"""
        exec("def foo(self):\nprint('bad indent')")

    @pytest.mark.skip(reason="SyntaxError TODO")
    def test_syntax_error_never_closed(self):
        """测试语法错误 - 未闭合括号"""
        exec("print('hello'")

    @pytest.mark.skip(reason="SyntaxError TODO")
    def test_syntax_error_invalid_name(self):
        """测试语法错误 - 无效变量名"""
        exec("1var = 42")

    @pytest.mark.skip(reason="SyntaxError TODO")
    def test_syntax_error_invalid_decimal(self):
        """测试语法错误 - 无效十进制"""
        exec("a = 1.2e2.3")

    @pytest.mark.skip(reason="SyntaxError TODO")
    def test_syntax_error_invalid_oct(self):
        """测试语法错误 - 无效八进制"""
        exec("a = 0123")
