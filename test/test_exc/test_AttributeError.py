import re

import pytest

from kawaiitb.handlers.defaults import AttributeErrorHandler
from test.utils.utils import KTBTestBase


class TestAttributeError(KTBTestBase, console_output=False, packing_handler=AttributeErrorHandler):
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
        - "attrerr_partinit_module" 文件
        - "__attrerr_partinit_module_2nd" 文件
        - "__attrerr_partinit_module_3rd" 文件

    """

    # region 辅助工具

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
    # endregion

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
                     "attrfun2", "_attrfun3", "_Foo__attrfun4", "__str__"],
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
                     "_attrfun3", "_Foo__attrfun4", "__str__"]
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
                     "attrfun2", "_attrfun3", "_Foo__attrfun4", "__str__"]
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
                     "_attrfun3", "_Foo__attrfun4", "__str__"],
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
            exclude=["attrfun1", "attrfun2", "_attrfun3", "_Foo__attrfun4",
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
            include=["attrfun1", "attrfun2", "_attrfun3", "_Foo__attrfun4"],
            exclude=["attrcon1", "attrcon2", "_attrcon3", "__attrcon4", "__str__"]
        )

    def test_custom_class_dunder_functions(self):
        """测试双下划线函数建议. 同上"""
        obj = self.Foo()
        with pytest.raises(AttributeError) as excinfo:
            obj.__brrro()  # noqa
        tbmsg = self._get_traceback_message(excinfo)
        self._assert_suggestions(tbmsg,
            include=["attrfun1", "attrfun2", "_attrfun3", "_Foo__attrfun4"],
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
            exclude=["attrfun1", "attrfun2", "_attrfun3", "_Foo__attrfun4",
                     "attrcon1", "attrcon2", "_attrcon3", "__attrcon4",
                     "__str__", "__dir__"]
        )

    # endregion

    # region 2. 模块的属性

    def test_module_function_call_similar(self):
        """测试模块相似函数调用建议"""
        import math
        with pytest.raises(AttributeError) as excinfo:
            math.sqr()  # noqa
        tbmsg = self._get_traceback_message(excinfo)
        self._assert_suggestions(tbmsg,
            include=["sqrt"],
            exclude=["exp", "pi"]
        )

    def test_module_attr_similar_function(self):
        """测试模块相似函数属性建议"""
        import math
        with pytest.raises(AttributeError) as excinfo:
            math.sqr  # noqa
        tbmsg = self._get_traceback_message(excinfo)
        self._assert_suggestions(tbmsg,
            include=["sqrt"],
            exclude=["exp", "pi"]
        )

    def test_module_constant_similar(self):
        """测试模块相似常量建议"""
        import math
        with pytest.raises(AttributeError) as excinfo:
            math.tai  # noqa
        tbmsg = self._get_traceback_message(excinfo)
        self._assert_suggestions(tbmsg,
            include=["tau"],
            exclude=["pi", "sqrt"]
        )

    def test_module_all_functions(self):
        """测试模块所有函数建议"""
        import math
        with pytest.raises(AttributeError) as excinfo:
            math.fooooo()  # noqa
        tbmsg = self._get_traceback_message(excinfo)
        self._assert_suggestions(tbmsg,
            include=["acos", "asin"],
            exclude=["pi", "tau"]
        )

    def test_module_all_constants(self):
        """测试模块所有常量建议"""
        import math
        with pytest.raises(AttributeError) as excinfo:
            math.fooooo  # noqa
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
            exclude=["capitalize"]
        )
        assert "..." not in tbmsg

    def test_builtin_all_methods(self):
        """测试内置对象所有方法"""
        with pytest.raises(AttributeError) as excinfo:
            "  str ing\n".foooo()  # noqa
        tbmsg = self._get_traceback_message(excinfo)
        self._assert_suggestions(tbmsg,
            include=["capitalize", "casefold"],
            exclude=["__str__", "__repr__", "zfill"]
        )
        assert "..." in tbmsg

    # endregion

    # region 4. 其他

    def test_attrerror_circular_import(self):
        """测试循环导入引发的AttributeError"""
        with pytest.raises(AttributeError) as excinfo:
            import test.utils.attrerr_partinit_module  # noqa
        tbmsg = self._get_traceback_message(excinfo)
        assert "attrerr_partinit_module.py" in tbmsg
        assert "__attrerr_partinit_module_2nd.py" in tbmsg
        assert "__attrerr_partinit_module_3rd.py" in tbmsg

    def test_attrerror_stdlib_rename(self):
        """测试模块与标准库重名引发的AttributeError"""
        with pytest.raises(AttributeError) as excinfo:
            import test.utils.keyword as keyword  # noqa
            _ = "class" in keyword.kwlist  # noqa
        tbmsg = self._get_traceback_message(excinfo)
        assert "模块 'keyword' 的名字覆盖了标准库模块。'kwlist' 存在于对应的标准库中。" in tbmsg

    def test_attrerror_stdlib_rename2(self):
        """测试变量与标准库重名引发的AttributeError"""
        with pytest.raises(AttributeError) as excinfo:
            keyword = "keyword"  # noqa
            _ = "class" in keyword.kwlist  # noqa
        tbmsg = self._get_traceback_message(excinfo)
        assert "变量 'keyword' 的名字覆盖了标准库模块。'kwlist' 存在于对应的标准库中。" in tbmsg
    # endregion

# AttributeError的情况。或不完整
#
# "'%.100s' object has no attribute '%U'"
# "'%.100s' object has no attribute '%U' and no __dict__ for setting new attributes"
# "type object '%.50s' has no attribute '%U'"
# "type object '%.100s' has no attribute '%U'"
# "'%.100s' object attribute '%U' is read-only"
# "readonly attribute"
# "object %.50s does not have %U method"
# "cannot delete attribute"
# "can't delete attribute"
# "This object has no __weakref__"
# "This object has no __dict__"
# "type object '%s' has no attribute '__annotations__'"
# "type object '%s' has no attribute '__annotate__'"
#
# "module '%U' has no attribute '%U'"
# "module has no attribute '%U'"
# "module '%U' has no attribute '%U' (consider renaming '%U' since it has the same name as the standard library module named '%U' and prevents importing that standard library module)"
# "module '%U' has no attribute '%U' (consider renaming '%U' if it has the same name as a library you intended to import)"
# "partially initialized module '%U' from '%U' has no attribute '%U' (most likely due to a circular import)"
# "partially initialized module '%U' has no attribute '%U' (most likely due to a circular import)"
# "cannot access submodule '%U' of module '%U' (most likely due to a circular import)"