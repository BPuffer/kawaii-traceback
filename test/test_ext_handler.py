import unittest

import kawaiitb

__CONFIG__ = {
    "translate_keys": {
        "__test__": {
            "extend": "neko_zh"
        }
    },
    "default_lang": "__test__"
}

class TestExceptionFormatting(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.traceback = kawaiitb.traceback
        kawaiitb.load_config(__CONFIG__)

    @classmethod
    def tearDownClass(cls):
        kawaiitb.unload()

    def test_pyyaml_exc(self):
        """普通的异常"""
        try:
            import pyyaml  # noqa
        except Exception as e:
            exc_format = "".join(self.traceback.format_exception(e))
            print(exc_format)