import unittest

import kawaiitb;kawaiitb.load()

class TestSyntaxError(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.traceback = kawaiitb.traceback

    @classmethod
    def tearDownClass(cls):
        kawaiitb.unload()

    def test_spelling_error_print(self):
        """测试拼写错误的print"""
        try:
            prant("awa")
        except Exception as e:
            exc_format = "".join(self.traceback.format_exception(e))
            print(exc_format)

    def test_spelling_error_numpy(self):
        """测试拼写错误的库中方法"""
        try:
            import numpy as np
            if False:
                np.arrat = np.array
            a = np.arrat([1, 2, 3])
        except Exception as e:
            exc_format = "".join(self.traceback.format_exception(e))
            print(exc_format)

    def test_missing_import(self):
        """测试忘记导入模块"""
        try:
            asyncio.run(asyncio.sleep(1))
        except Exception as e:
            exc_format = "".join(self.traceback.format_exception(e))
            print(exc_format)

    def test_missing_attribute(self):
        """测试不存在的属性"""
        try:
            person = type("Person", (), {})()
            person.nonexistent_attribute
        except Exception as e:
            exc_format = "".join(self.traceback.format_exception(e))
            print(exc_format)

    def test_circular_import(self):
        """测试循环导入"""
        try:
            from test import another
        except Exception as e:
            exc_format = "".join(self.traceback.format_exception(e))
            print(exc_format)

    def test_site_package_error(self):
        """测试site-package模块异常"""
        try:
            import scipy, numpy
            def f(x, y):
                return x * x + y * y + 1

            scipy.optimize.minimize(f, numpy.array([1, 1, 1]))
        except Exception as e:
            exc_format = "".join(self.traceback.format_exception(e))
            print(exc_format)