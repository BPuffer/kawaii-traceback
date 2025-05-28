from io import StringIO

import pytest
from unittest import mock
from test.utils.utils import KTBTestBase
from kawaiitb.handlers.defaults import EOFErrorHandler

class TestEOFError(KTBTestBase, console_output=True):
    @mock.patch("sys.stdin", StringIO(""))
    def test_eof_error(self):
        """测试EOFError"""
        with pytest.raises(EOFError) as exc_info:
            input()
        e = exc_info.value
        ktb, handler, msgs, tbmsg = self.pack_exc(EOFErrorHandler, e)
        self.try_print_exc(e)
        assert "EOFError" in tbmsg

