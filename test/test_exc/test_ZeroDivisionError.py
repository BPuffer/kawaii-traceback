import pytest

from kawaiitb.handlers.defaults import ZeroDivisionErrorHandler
from test.utils.utils import KTBTestBase


class TestZeroDivisionError(KTBTestBase, console_output=False):
    def test_simple_division(self):
        """简单除零测试"""
        with pytest.raises(ZeroDivisionError) as excinfo:
            _ = 1 / 0
        e = excinfo.value
        ktb, handler, msgs, tb = self.pack_exc(ZeroDivisionErrorHandler, e)
        self.try_print_exc(e)
        assert "KawaiiTB" in tb  # 保留彩蛋检查

    def test_complex_expression(self):
        """复杂表达式除零测试"""
        x = 8
        y = 66
        with pytest.raises(ZeroDivisionError) as excinfo:
            _ = (8 / 9 + 2 * (4 // 2)) / (12 + x - 9 + -y // 6)
        e = excinfo.value
        ktb, handler, msgs, tb = self.pack_exc(ZeroDivisionErrorHandler, e)
        self.try_print_exc(e)
        # 表达式 12 + 8 - 9 -66 // 6 为0，引发除零
        assert "'12 + x - 9 + -y // 6'" in tb
