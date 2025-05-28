import re

import pytest
from kawaiitb.handlers.defaults import AttributeErrorHandler
from test.utils.utils import KTBTestBase


class TestAttributeError(KTBTestBase, console_output=True):
    """
    完成TestAttributeError。要完成判断的有以下几类：
    1. 自定义类的属性
    - 表达式 f.attrcin1(): 应该猜出函数 f.attrfun1(), 不应该出现 attrcon1, attrcon2, attrfun2, _attrcon3, __attrcon4
    - 表达式 f.attrfin1: 应该猜出函数对象 attrfun1, 不应该出现 attrcon1, attrcon2, attrfun2, _attrfun3, __attrfun4
    - 表达式 f.attrcin1: 应该猜出常量 attrcon1, 不应该出现 attrcon2, attrfun1, attrfun2, _attrcon3, __attrcon4
    - 表达式 f.brrrrrro(): 应该列出函数 attrfun1() 和 attr_fun2(), 不应该出现 attrcon1, attrcon2, _attrfun3, __attrfun4
    - 表达式 f.brrrrrro: 应该列出常量 attrcon1 和 attrcon2, 不应该出现 attrfun1, attrfun2, _attrfun3, __attrfun4
    - 表达式 f._brrro(): 应该列出所有函数, 不应该出现常量, 不应该出现魔法方法
    - 表达式 f.__brrro(): 应该列出所有函数, 不应该出现常量, 不应该出现魔法方法
    - 表达式 f._brrro: 应该列出所有常量, 不应该出现函数
    - 表达式 f.__brrro: 应该列出所有常量, 不应该出现函数
    - 表达式 f.__inot__(): 应该列出所有魔法方法, 不应该出现函数, 不应该出现常量
    2. 模块的属性
    - 表达式 math.sqr(): 应该猜出函数 sqrt(), 不应该出现其他函数如exp, 不应该出现常量如 pi
    - 表达式 math.sqr: 应该猜出函数对象 sqrt, 不应该出现其他函数如exp, 不应该出现常量如 pi
    - 表达式 math.tai: 应该猜出常量 tau, 不应该出现 sqrt 或者 pi
    - 表达式 math.foo(): 应该列出 math 中的所有函数(如sqrt), 不应该出现常量(如pi)
    - 表达式 math.foo: 应该列出 math 中的所有常量(如pi), 不应该出现函数(如sqrt)
    3. 内置对象的属性
    - 表达式 "  str ing\n".strup(): 应该猜出函数 strip(), 不应该出现其他函数如 lower
    - 表达式 "  str ing\n".foooo(): 应该列出所有函数, 不应该出现魔法方法
    4. 其他
    - 循环导入时会产生特殊的 AttributeError.
      从 test.utils.attrerr_partinit_module 导入 entry 函数, 然后
      调用 entry("I'm sure I wan't to raise an AttributeError") 会产生 AttributeError. 捕捉这个异常.
      输出结果中应该包含:
        - "test.utils.attrerr_partinit_module" 字样
        - "test.utils.__attrerr_partinit_module_2nd" 字样
        - "test.utils.__attrerr_partinit_module_3rd" 字样

    """

    class Foo:
        attrcon1 = 1
        attrcon2 = 2
        _attrcon3 = 3
        __attrcon4 = 4
        attrfun1 = lambda self: 3
        attrfun2 = lambda self: 4
        _attrfun3 = lambda self: 5
        __attrfun4 = lambda self: 6

    def _assert_suggestions(self, tbmsg, include=(), exclude=()):
        """辅助函数：验证建议内容"""
        pattern = r"['\"]([\w_]+)['\"]"

        suggestions = re.findall(pattern, tbmsg)
        for item in include:
            assert item in suggestions
        for item in exclude:
            assert item not in suggestions

    def _get_traceback_message(self, excinfo):
        """辅助函数：获取 traceback 信息"""
        self.try_print_exc(excinfo.value)
        *_, tbmsg = self.pack_exc(AttributeErrorHandler, excinfo.value)
        return tbmsg

    # region 1. 自定义类的属性

    def test_custom_class_func_call_similar(self):
        """
        测试相似函数调用建议
        obj.attrcin1()这样明显的typo应该明确地指向obj.attrfun1()
        """
        obj = self.Foo()
        with pytest.raises(AttributeError) as excinfo:
            obj.attrcin1()  # noqa
        tbmsg = self._get_traceback_message(excinfo)
        self._assert_suggestions(tbmsg,
            include=["attrfun1"],
            exclude=["attrcon1", "attrcon2", "_attrcon3", "__attrcon4",
                     "attrfun2", "_attrfun3", "__attrfun4", "__str__"],
        )

    def test_custom_class_attr_similar_function(self):
        """
        测试相似函数属性建议
        obj.attrfin1应该明确地指向obj.attrfun1.
        作为常量的attrcon1也是一个考虑点, 因为面向对象之形中,
        使用obj.attrfin1却不是调用的情况少之又少
        """
        obj = self.Foo()
        with pytest.raises(AttributeError) as excinfo:
            obj.attrfin1  # noqa
        tbmsg = self._get_traceback_message(excinfo)
        self._assert_suggestions(tbmsg,
            include=["attrfun1", "attrcon1"],
            exclude=["attrcon2", "_attrcon3", "__attrcon4", "attrfun2",
                     "_attrfun3", "__attrfun4", "__str__"]
        )

    def test_custom_class_attr_similar_constant(self):
        """
        测试相似常量属性建议
        obj.attrcin1应该明确地指向obj.attrcon1.
        作为函数的attrfun1将不会被考虑. 因为有匹配度更高的常量.
        """
        obj = self.Foo()
        with pytest.raises(AttributeError) as excinfo:
            obj.attrcin1  # noqa
        tbmsg = self._get_traceback_message(excinfo)
        self._assert_suggestions(tbmsg,
            include=["attrcon1"],
            exclude=["attrcon2", "_attrcon3", "__attrcon4", "attrfun1",
                     "attrfun2", "_attrfun3", "__attrfun4", "__str__"]
        )

    def test_custom_class_all_functions(self):
        """
        测试列出所有函数
        我们找不到任何足够匹配的函数, 所以应该列出所有函数.
        """
        obj = self.Foo()
        with pytest.raises(AttributeError) as excinfo:
            obj.brrrrrro()  # noqa
        tbmsg = self._get_traceback_message(excinfo)
        self._assert_suggestions(tbmsg,
            include=["attrfun1", "attrfun2"],
            exclude=["attrcon1", "attrcon2" "_attrcon3", "__attrcon4",
                     "_attrfun3", "__attrfun4", "__str__"],
        )

    def test_custom_class_all_constants(self):
        """
        测试列出所有常量
        我们找不到任何足够匹配的常量, 所以应该列出所有常量.
        """
        obj = self.Foo()
        with pytest.raises(AttributeError) as excinfo:
            obj.brrrrrro  # noqa
        tbmsg = self._get_traceback_message(excinfo)
        self._assert_suggestions(tbmsg,
            include=["attrcon1", "attrcon2"],
            exclude=["attrfun1", "attrfun2", "_attrfun3", "__attrfun4",
                     "_attrcon3", "__attrcon4", "__str__"]
        )

    def test_custom_class_private_functions(self):
        """
        测试私有函数建议
        一旦尝试了调用私有函数, 我们就应该将所有私有的函数考虑在内
        """
        obj = self.Foo()
        with pytest.raises(AttributeError) as excinfo:
            obj._brrro()  # noqa
        tbmsg = self._get_traceback_message(excinfo)
        self._assert_suggestions(tbmsg,
            include=["attrfun1", "attrfun2", "_attrfun3", "__attrfun4"],
            exclude=["attrcon1", "attrcon2", "_attrcon3", "__attrcon4", "__str__"]
        )

    def test_custom_class_dunder_functions(self):
        """测试双下划线函数建议. 同上"""
        obj = self.Foo()
        with pytest.raises(AttributeError) as excinfo:
            obj.__brrro()  # noqa
        tbmsg = self._get_traceback_message(excinfo)
        self._assert_suggestions(tbmsg,
            include=["attrfun1", "attrfun2", "_attrfun3", "__attrfun4"],
            exclude=["attrcon1", "attrcon2", "_attrcon3", "__attrcon4", "__str__"]
        )

    def test_custom_class_magic_methods(self):
        """
        测试魔法方法建议
        一旦尝试了调用魔法方法, 我们就不应该考虑任何常规方法.
        魔法方法使用前后双下划线判别.
        另外, 案例中的 __inot__ 已经足够明显地指向 __init__ 方法了.
        所以不应该出现其他魔法方法.
        """
        obj = self.Foo()
        with pytest.raises(AttributeError) as excinfo:
            obj.__inot__()  # noqa
        tbmsg = self._get_traceback_message(excinfo)
        self._assert_suggestions(tbmsg,
            include=["__init__"],
            exclude=["attrfun1", "attrfun2", "_attrfun3", "__attrfun4",
                     "attrcon1", "attrcon2", "_attrcon3", "__attrcon4",
                     "__str__", "__dir__"]
        )

    # endregion

    # region 2. 模块的属性

    def test_module_function_call_similar(self):
        """测试模块相似函数调用建议"""
        with pytest.raises(AttributeError) as excinfo:
            math.sqr()  # noqa
        tbmsg = self._get_traceback_message(excinfo)
        self._assert_suggestions(tbmsg,
            include=["sqrt"],
            exclude=["exp", "pi"]
        )

    def test_module_attr_similar_function(self):
        """测试模块相似函数属性建议"""
        with pytest.raises(AttributeError) as excinfo:
            math.sqr  # noqa
        tbmsg = self._get_traceback_message(excinfo)
        self._assert_suggestions(tbmsg,
            include=["sqrt"],
            exclude=["exp", "pi"]
        )

    def test_module_constant_similar(self):
        """测试模块相似常量建议"""
        with pytest.raises(AttributeError) as excinfo:
            math.tai  # noqa
        tbmsg = self._get_traceback_message(excinfo)
        self._assert_suggestions(tbmsg,
            include=["tau"],
            exclude=["pi", "sqrt"]
        )

    def test_module_all_functions(self):
        """测试模块所有函数建议"""
        with pytest.raises(AttributeError) as excinfo:
            math.foo()  # noqa
        tbmsg = self._get_traceback_message(excinfo)
        self._assert_suggestions(tbmsg,
            include=["sqrt", "cos"],
            exclude=["pi", "tau"]
        )

    def test_module_all_constants(self):
        """测试模块所有常量建议"""
        with pytest.raises(AttributeError) as excinfo:
            math.foo  # noqa
        tbmsg = self._get_traceback_message(excinfo)
        self._assert_suggestions(tbmsg,
            include=["pi", "tau"],
            exclude=["sqrt", "cos"]
        )

    # endregion

    # region 3. 内置对象的属性

    def test_builtin_method_similar(self):
        """测试内置对象相似方法"""
        with pytest.raises(AttributeError) as excinfo:
            "  str ing\n".strup()  # noqa
        tbmsg = self._get_traceback_message(excinfo)
        self._assert_suggestions(tbmsg,
            include=["strip"],
            exclude=["lower"]
        )

    def test_builtin_all_methods(self):
        """测试内置对象所有方法"""
        with pytest.raises(AttributeError) as excinfo:
            "  str ing\n".foooo()  # noqa
        tbmsg = self._get_traceback_message(excinfo)
        self._assert_suggestions(tbmsg,
            include=["strip", "lower"],
            exclude=["__str__", "__repr__"]
        )
        # 应包含普通方法
        assert "strip()" in tbmsg
        assert "lower()" in tbmsg
        # 不应包含魔法方法
        assert "__str__" not in tbmsg
        assert "__repr__" not in tbmsg

    # endregion

    # region 4. 其他

    def test_attrerror_circular_import(self):
        """测试循环导入引发的AttributeError"""
        from test.utils.attrerr_partinit_module import entry
        with pytest.raises(AttributeError) as excinfo:
            entry("I'm sure I wan't to raise an AttributeError")
        tbmsg = self._get_traceback_message(excinfo)

        # 验证包含特定模块路径
        assert "test.utils.attrerr_partinit_module" in tbmsg
        assert "test.utils.__attrerr_partinit_module_2nd" in tbmsg
        assert "test.utils.__attrerr_partinit_module_3rd" in tbmsg

    # endregion
