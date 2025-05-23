import unittest
import kawaiitb
from kawaiitb import KTBException

__CONFIG__ = {
    "translate_keys": {
        "__test__": {
            "extend": "neko_zh"
        }
    },
    "default_lang": "__test__"
}

class KTBTestCase(unittest.TestCase):
    preview = False

    def try_preview(self, e):
        if self.preview:
            print("".join(self.traceback.format_exception(e)))

    def __init_subclass__(cls, preview=False, **kwargs):
        super().__init_subclass__(**kwargs)
        cls.preview = preview

    def pack_exc(self, HandlerType, exc):
        ktb = KTBException.from_exception(exc)
        handler = HandlerType(type(exc), exc, exc.__traceback__)
        assert handler.can_handle(ktb)
        messages = list(handler.handle(ktb))
        return ktb, handler, messages, "".join(messages)

    @classmethod
    def setUpClass(cls):
        cls.traceback = kawaiitb.traceback
        kawaiitb.load_config(__CONFIG__)

    @classmethod
    def tearDownClass(cls):
        kawaiitb.unload()