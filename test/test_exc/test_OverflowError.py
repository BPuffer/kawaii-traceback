import math

import pytest

from kawaiitb.handlers.defaults import OverflowErrorHandler
from test.utils.utils import KTBTestBase


class TestOverflowError(KTBTestBase, console_output=False):
    def test_math_exp(self):
        """测试math.exp()引发的OverflowError"""
        with pytest.raises(OverflowError) as excinfo:
            a = math.exp(1000)
        e = excinfo.value
        self.try_print_exc(e)
        self.pack_exc(OverflowErrorHandler, e)
