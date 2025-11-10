import io

import pytest

import kawaiitb
from kawaiitb import kraceback
from test.utils.utils import KTBTestBase

class TestExceptionFromLibs(KTBTestBase, console_output=True, packing_handler=kawaiitb.ErrorSuggestHandler):
    def test_from_std_lib(self):
        """测试从stdlib引发的错误，这里尝试错误地解码SGVsbG8为base64"""
        with pytest.raises(Exception) as excinfo:
            import base64
            base64.b64decode("SGVsbG8")

        stream = io.StringIO()
        kraceback.print_exception(excinfo.value, file=stream)
        fulltb = stream.getvalue()
        assert "[base64" in fulltb

    def test_from_third_party_lib(self):
        """测试从third party lib引发的错误，此处使用numpy计算维度不符的数组"""
        with pytest.raises(Exception) as excinfo:
            import numpy as np
            np.random.uniform(low=[1, 2], high=[4, 5, 6], size=(3))

        stream = io.StringIO()
        kraceback.print_exception(excinfo.value, file=stream)
        fulltb = stream.getvalue()
        assert "[numpy" in fulltb


