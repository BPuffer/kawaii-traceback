import unittest
import kawaiitb;
import unittest

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
    
    def test_binop_error(self):
        """测试AST BinOp"""
        try:
            a = "s" + 1
        except TypeError as e:
            exc_format = "".join(self.traceback.format_exception(e))
            print(exc_format)
            #   a = "s" + 1
            assert "~~~~^~~" in exc_format, exc_format
    
    def test_subscript_error(self):
        """测试AST Subscript"""
        try:
            d = {"a": 1}["b"]
        except KeyError as e:
            exc_format = "".join(self.traceback.format_exception(e))
            print(exc_format)
            #   d = {"a": 1}["b"]
            assert "~~~~~~~~^^^^^" in exc_format, exc_format
    
    def test_syntax_error_invalid_lex(self):
        """测试语法错误 - 无效词法"""
        try:
            exec("what can i say?")
        except SyntaxError as e:
            exc_format = "".join(self.traceback.format_exception(e))
            print(exc_format)
    
    def test_syntax_error_unexpected_end(self):
        """测试语法错误 - 不预期结束"""
        try:
            exec("1 + 2 *")
        except SyntaxError as e:
            exc_format = "".join(self.traceback.format_exception(e))
            print(exc_format)
    
    def test_syntax_error_invalid_indent(self):
        """测试语法错误 - 无效缩进"""
        try:
            exec("def foo(self):\nprint('bad indent')")
        except IndentationError as e:  # IndentationError 是 SyntaxError 的子类
            exc_format = "".join(self.traceback.format_exception(e))
            print(exc_format)
    
    def test_syntax_error_never_closed(self):
        """测试语法错误 - 未闭合括号"""
        try:
            exec("print('hello'")
        except SyntaxError as e:
            exc_format = "".join(self.traceback.format_exception(e))
            print(exc_format)
    
    def test_syntax_error_invalid_name(self):
        """测试语法错误 - 无效变量名"""
        try:
            exec("1var = 42")
        except SyntaxError as e:
            exc_format = "".join(self.traceback.format_exception(e))
            print(exc_format)
    
    def test_syntax_error_invalid_decimal(self):
        """测试语法错误 - 无效十进制"""
        try:
            exec("a = 1.2e2.3")
        except SyntaxError as e:
            exc_format = "".join(self.traceback.format_exception(e))
            print(exc_format)
    
    def test_syntax_error_invalid_oct(self):
        """测试语法错误 - 无效八进制"""
        try:
            exec("a = 0123")
        except SyntaxError as e:
            exc_format = "".join(self.traceback.format_exception(e))
            print(exc_format)
