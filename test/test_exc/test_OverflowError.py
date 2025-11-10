import pytest

from kawaiitb.handlers.defaults import OverflowErrorHandler
from test.utils.utils import KTBTestBase


class TestOverflowError(KTBTestBase, console_output=False, packing_handler=OverflowErrorHandler):
    def test_math_exp(self):
        """测试math.exp()引发的OverflowError"""
        import math
        with pytest.raises(OverflowError) as excinfo:
            a = math.exp(1000)
        e = excinfo.value
        self.try_print_exc(e)
        tbmsg = self._get_traceback_message(excinfo)
        assert "OverflowError" in tbmsg

    def test_time_localtime(self):
        """测试time.localtime()引发的OverflowError"""
        import time
        with pytest.raises(OverflowError) as excinfo:
            time.localtime(10**100)
        e = excinfo.value
        self.try_print_exc(e)
        tbmsg = self._get_traceback_message(excinfo)
        assert "OverflowError" in tbmsg
