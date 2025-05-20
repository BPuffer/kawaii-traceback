import json
import unittest
import sys
import kawaiitb; kawaiitb.load()

__CONFIG__ = {
    "translate_keys": {
        "__test__": {
            "extend": "neko_zh"
            # "stack.summary": "stack.summary",  # Traceback (most recent call last):\n
            # "frame.location.with_column": "{{'frame.location.with_column': {{'file':r'{file}', 'lineno':'{lineno}', 'name':'{name}', 'colno':'{colno}' }}}}\n",  #   File "test.py", line 1, in <module>\n
            # "frame.location.linetext": "{{'frame.location.linetext':{{'line':r'{line}' }} }}\n",  #     raise Exception("test")\n
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

    def test_normal_exc(self):
        """普通的异常"""
        try:
            raise Exception("test")
        except Exception as e:
            exc_format = "".join(self.traceback.format_exception(e))
            print(exc_format)

    def test_nested_exception(self):
        """异常追溯"""
        try:
            def f1():
                a = 1 / 0

            def f2():
                f1()

            def f3():
                f2()

            f3()
        except Exception as e:
            exc_format = "".join(self.traceback.format_exception(e))
            print(exc_format)

    def test_exception_cause(self):
        """cause链"""
        try:
            raise Exception("test")
        except Exception as e:
            try:
                raise Exception("test2") from e
            except Exception as e2:
                exc_format = "".join(self.traceback.format_exception(e2))
                print(exc_format)

    def test_external_module_error(self):
        """测试工作区其他模块异常"""
        try:
            from dir_.at import raise_error
            raise_error()
        except Exception as e:
            exc_format = "".join(self.traceback.format_exception(e))
            print(exc_format)

