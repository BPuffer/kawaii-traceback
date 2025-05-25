"""
[禁止pytest断言重写] PYTEST_DONT_REWRITE
"""

import pytest
from ..utils.utils import KTBTestBase
from kawaiitb.handlers.defaults import AssertionErrorHandler


class TestAssertionError(KTBTestBase, console_output=False):
    def test_compare_assertion(self):
        """测试比较断言"""

        with pytest.raises(AssertionError) as excinfo:
            a, b = 1, 2
            assert a == b

        e = excinfo.value
        self.try_print_exc(e)
        ktb, handler, msgs, tbmsg = self.pack_exc(AssertionErrorHandler, e)

        assert "a == b" in tbmsg, f"a == b not in {tbmsg}"
        assert "a=1" in tbmsg, f"a=1 not in {tbmsg}"
        assert "b=2" in tbmsg, f"b=2 not in {tbmsg}"

    def test_boolop_assertion(self):
        """测试布尔运算断言"""
        with pytest.raises(AssertionError) as excinfo:
            x, y = True, False
            assert x and y
        e = excinfo.value
        self.try_print_exc(e)
        ktb, handler, msgs, tbmsg = self.pack_exc(AssertionErrorHandler, e)
        assert "x and y" in tbmsg, f"x and y not in {tbmsg}"
        assert "x=True" in tbmsg, f"x=True not in {tbmsg}"
        assert "y=False" in tbmsg, f"y=False not in {tbmsg}"
        assert "x and y=False" in tbmsg, f"x and y=False not in {tbmsg}"

    def test_simple_var_assertion(self):
        """测试简单变量断言"""
        with pytest.raises(AssertionError) as excinfo:
            flag = False
            assert flag
        e = excinfo.value
        self.try_print_exc(e)
        ktb, handler, msgs, tbmsg = self.pack_exc(AssertionErrorHandler, e)
        assert "flag" in tbmsg, f"flag not in {tbmsg}"
        assert "flag=False" in tbmsg, f"flag=False not in {tbmsg}"

    def test_boolfunc_call_assertion_const(self):
        """测试布尔函数调用常量断言"""
        with pytest.raises(AssertionError) as excinfo:
            def is_even(n): return n % 2 == 0

            assert is_even(3)
        e = excinfo.value
        self.try_print_exc(e)
        ktb, handler, msgs, tbmsg = self.pack_exc(AssertionErrorHandler, e)
        # 布尔函数调用时, 不应该显示总体参数, 且3是常量, 也不应该显示
        assert "=3" not in tbmsg, f"=3 in {tbmsg}"

    def test_boolfunc_call_assertion_var(self):
        """测试布尔函数调用变量断言"""
        with pytest.raises(AssertionError) as excinfo:
            def is_even(n): return n % 2 == 0

            num = 3
            assert is_even(num)
        e = excinfo.value
        self.try_print_exc(e)
        ktb, handler, msgs, tbmsg = self.pack_exc(AssertionErrorHandler, e)
        # 布尔函数调用时，应该显示变量名及其值
        assert "num=3" in tbmsg, f"num=3 not in {tbmsg}"
        # 但不应显示函数本身
        assert ")=" not in tbmsg, f")= in {tbmsg}"

    def test_normfunc_call_assertion_const(self):
        """测试普通函数调用常量断言"""
        with pytest.raises(AssertionError) as excinfo:
            def get_var(n): return None if n > 0 else n

            assert get_var(2)
        e = excinfo.value
        self.try_print_exc(e)
        ktb, handler, msgs, tbmsg = self.pack_exc(AssertionErrorHandler, e)
        # 普通函数调用时，常量参数不应显示
        assert "=2" not in tbmsg, f"=2 in {tbmsg}"
        # 但应显示函数调用结果
        assert "get_var(2)=None" in tbmsg, f"get_var(2)=None not in {tbmsg}"

    def test_normfunc_call_assertion_var(self):
        """测试普通函数调用变量断言"""
        with pytest.raises(AssertionError) as excinfo:
            def get_var(n): return None if n > 0 else n

            num = 2
            assert get_var(num)
        e = excinfo.value
        self.try_print_exc(e)
        ktb, handler, msgs, tbmsg = self.pack_exc(AssertionErrorHandler, e)
        # 普通函数调用时，变量参数不会显示
        assert "num=2" not in tbmsg, f"num=2 in {tbmsg}"
        # 也应显示函数调用结果
        assert "get_var(num)=None" in tbmsg, f"get_var(num)=None not in {tbmsg}"

    def test_complex_expr_assertion(self):
        """测试复杂表达式断言"""
        with pytest.raises(AssertionError) as excinfo:
            x, y = 5, 10
            assert x * 2 < y / 2
        e = excinfo.value
        self.try_print_exc(e)
        ktb, handler, msgs, tbmsg = self.pack_exc(AssertionErrorHandler, e)
        assert "x * 2 < y / 2" in tbmsg, f"x * 2 < y / 2 not in {tbmsg}"
        assert "x * 2=10" in tbmsg, f"x * 2=10 not in {tbmsg}"
        assert "y / 2=5.0" in tbmsg, f"y / 2=5.0 not in {tbmsg}"
