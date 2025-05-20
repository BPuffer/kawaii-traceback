import sys

import kawaiitb; kawaiitb.load('en_us')
traceback = kawaiitb.traceback
assert kawaiitb.rc._lang == 'en_us', f"{kawaiitb.rc._lang=}, {kawaiitb.rc.langs=}"

out_to_here = sys.stderr

def fooooooooooooooooooooooooooooooooooooooo():
    print("\n", "=" * 50, "\n", file=out_to_here)

def test_syntax_error_invalid_lex():
    """测试语法错误 - 无效词法"""
    try:
        exec("what can i say?")
    except SyntaxError as e:
        exc_format = "".join(traceback.format_exception(e))
        print(exc_format)


if __name__ == '__main__1':

    fooooooooooooooooooooooooooooooooooooooo()
    """
    普通的异常
    """
    try:
        raise Exception("test")
    except Exception as e:
        traceback.print_exception(e, file=out_to_here)

    fooooooooooooooooooooooooooooooooooooooo()
    """
    嵌套的异常
    """
    try:
        def f1():
            a   =   1   /   0


        def f2():
            f1()


        def f3():
            f2()


        f3()
    except Exception as e:
        traceback.print_exception(e, file=out_to_here)

    fooooooooooooooooooooooooooooooooooooooo()
    """
    测试拼写错误的建议
    """
    try:
        # prant = print
        prant("awa")
    except Exception as e:
        traceback.print_exception(e, file=out_to_here)


    fooooooooooooooooooooooooooooooooooooooo()
    """
    测试拼写错误的建议
    """
    try:
        import numpy as np
        # np.arrat = np.array
        a = np.arrat([1, 2, 3])
    except Exception as e:
        traceback.print_exception(e, file=out_to_here)

    fooooooooooooooooooooooooooooooooooooooo()
    """
    测试忘记导入的建议
    """
    try:
        # import asyncio
        asyncio.run(asyncio.sleep(1))
    except Exception as e:
        traceback.print_exception(e, file=out_to_here)

    fooooooooooooooooooooooooooooooooooooooo()
    """
    测试BinOp提示标记锚位置
    """
    try:
        a = 1 / 0
    except ZeroDivisionError as e:
        try:
            a = "s" + 1
        except TypeError as e:
            traceback.print_exception(e, file=out_to_here)

    fooooooooooooooooooooooooooooooooooooooo()
    """
    测试Subscript提示标记锚位置
    """
    try:
        d = {"a": 1}["b"]
    except Exception as e:
        traceback.print_exception(e, file=out_to_here)

    fooooooooooooooooooooooooooooooooooooooo()
    """
    测试不存在的属性
    """
    try:
        class Person:
            def __init__(self, name, age):
                self.name = name
                self.age = age

        person = Person("Alice", 30)
        person.nonexistent_attribute
    except Exception as e:
        traceback.print_exception(e, file=out_to_here)

    fooooooooooooooooooooooooooooooooooooooo()
    """
    测试异常的cause
    """
    try:
        raise Exception("test")
    except Exception as e:
        try:
            raise Exception("test2") from e
        except Exception as e:
            traceback.print_exception(e, file=out_to_here)

    fooooooooooooooooooooooooooooooooooooooo()
    """
    测试异常的context
    """
    try:
        import another
        another.hello()
    except Exception as e:
        traceback.print_exception(e, file=out_to_here)

    fooooooooooooooooooooooooooooooooooooooo()
    """
    测试语法异常的全指锚1
    """
    try:
        exec("what can i say?")
    except Exception as e:
        traceback.print_exception(e, file=out_to_here)

    fooooooooooooooooooooooooooooooooooooooo()
    """
    测试语法异常的全指锚2
    """
    try:
        exec("1 + 2 *")
    except Exception as e:
        traceback.print_exception(e, file=out_to_here)

    fooooooooooooooooooooooooooooooooooooooo()
    """
    测试在工作区其他模块中产生的异常
    """
    try:
        from dir_.at import raise_error
        raise_error()
    except Exception as e:
        traceback.print_exception(e, file=out_to_here)

    fooooooooooooooooooooooooooooooooooooooo()
    """
    测试在site-package中的模块里产生的异常
    """
    try:
        from dir_.at import scipy_error

        scipy_error()
    except Exception as e:
        traceback.print_exception(e, file=out_to_here)

    fooooooooooooooooooooooooooooooooooooooo()
    """
    测试在lib中的模块里产生的异常
    """
    try:
        import asyncio
        async def f():
            await asyncio.sleep(0)
            raise Exception("test")
        asyncio.run(f())
    except Exception as e:
        traceback.print_exception(e, file=out_to_here)

    fooooooooooooooooooooooooooooooooooooooo()
    """
    测试最大嵌套深度溢出
    """
    def f(e):
        raise f(Exception("test")) from e

    try:
        f(Exception("test"))
    except Exception as e:
        traceback.print_exception(e, file=out_to_here)

    fooooooooooooooooooooooooooooooooooooooo()
    """
    测试异常的cause from None
    """
    try:
        raise Exception("test") from None
    except Exception as e:
        traceback.print_exception(e, file=out_to_here)

    fooooooooooooooooooooooooooooooooooooooo()
    """
    测试异常的__notes__
    """
    try:
        class CustomException(Exception):
            def __init__(self, *args):
                super().__init__(*args)
                self.__notes__ = ["note1", "note2"]

        raise CustomException("test")
    except Exception as e:
        traceback.print_exception(e, file=out_to_here)




