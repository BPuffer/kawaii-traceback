import ast
import linecache
import sys
from typing import Generator

from kawaiitb.runtimeconfig import rc
from kawaiitb.kraceback import KTBException
from kawaiitb.kwihandler import ErrorSuggestHandler
from kawaiitb.utils.fromtraceback import compute_suggestion_error


__all__ = [
    "SyntaxErrorSuggestHandler",
    "ImportErrorSuggestHandler",
    "NameAttributeErrorSuggestHandler",
    # 这些属于原生增强，优先级都是1.1

]


@KTBException.register
class SyntaxErrorSuggestHandler(ErrorSuggestHandler, priority=1.1):
    """
    本处理器模仿原生的语法错误处理器，为语法错误添加额外的锚点指示
    """

    def __init__(self, exc_type, exc_value, exc_traceback, *, limit=None,
                 lookup_lines=True, capture_locals=False, compact=False,
                 max_group_width=15, max_group_depth=10, _seen=None):
        super().__init__(exc_type, exc_value, exc_traceback)
        if exc_type and issubclass(exc_type, SyntaxError):
            self.filename = exc_value.filename
            lno = exc_value.lineno
            self.lineno = str(lno) if lno is not None else None
            end_lno = exc_value.end_lineno
            self.end_lineno = str(end_lno) if end_lno is not None else None
            self.text = exc_value.text
            self.offset = exc_value.offset
            self.end_offset = exc_value.end_offset
            self.msg = exc_value.msg

    @classmethod
    def translation_keys(cls):
        return {}  # 翻译键均由默认配置提供，不需要额外的翻译键

    def can_handle(self, ktb_exc) -> bool:
        return issubclass(ktb_exc.exc_type, SyntaxError)

    def handle(self, ktb_exc) -> Generator[str, None, None]:
        r"""
        (-) Traceback (most recent call last):
        (-)   File "C:\Users\BPuffer\Desktop\kawaii-traceback\main.py", line 139:8, in <module>
        (-)     exec("what can i say?")
        (1)   File "<string>", line 1
        (2)     what can i say?
        (3)          ^^^
        (4) SyntaxError: invalid syntax (<string>, line 1)
        """
        if self.lineno is not None:
            # part (1)
            yield rc.translate("frame.location.without_name",
                               file=self.filename or "<string>",  # repr转义
                               lineno=self.lineno, )

        text = self.text
        if text is not None:
            rtext = text.rstrip('\n')
            ltext = rtext.lstrip(' \n\f')
            spaces = len(rtext) - len(ltext)
            # part (2)
            yield rc.translate("frame.location.linetext",
                               line=ltext)

            if self.offset is not None:
                offset = self.offset
                end_offset = self.end_offset if self.end_offset not in {None, 0} else offset
                if offset == end_offset or end_offset == -1:
                    end_offset = offset + 1

                colno = offset - 1 - spaces
                end_colno = end_offset - 1 - spaces
                if colno >= 0:
                    # part (3)
                    # caretspace = ((c if c.isspace() else ' ') for c in ltext[:colno])
                    # yield '    {}{}'.format("".join(caretspace), ('^' * (end_colno - colno) + "\n"))
                    anchor_len = end_colno - colno
                    yield rc.anchors('    ' + ' ' * colno, 0, 0, anchor_len, anchor_len, crlf=True)

        msg = self.msg or "<no detail available>"
        # part (4)
        yield from super().handle(ktb_exc)


@KTBException.register
class ImportErrorSuggestHandler(ErrorSuggestHandler, priority=1.1):
    """
    本处理器模仿原生的ImportError的拼写错误检测
    为导入中的拼写错误添加额外的正确拼写提示
    """

    def __init__(self, exc_type, exc_value, exc_traceback, *, limit=None,
                 lookup_lines=True, capture_locals=False, compact=False,
                 max_group_width=15, max_group_depth=10, _seen=None):
        super().__init__(exc_type, exc_value, exc_traceback)

        self._can_handle = issubclass(exc_type, ImportError) and getattr(exc_value, "name_from", None) is not None

        self.suggestion = None
        if self._can_handle:
            self.wrong_name = getattr(exc_value, "name_from")
            self.suggestion = compute_suggestion_error(exc_value, exc_traceback, self.wrong_name)

    def can_handle(self, ktb_exc) -> bool:
        return self._can_handle

    @classmethod
    def translation_keys(cls):
        return {
            "default": {
                "native.import_error_suggestion.hint": "Did you mean '{suggestion}'?",
            },
            "zh_hans": {
                "native.import_error_suggestion.hint": "你可能是想导入'{suggestion}'",
            }
        }

    def handle(self, ktb_exc) -> Generator[str, None, None]:
        yield from super().handle(ktb_exc)
        if self.suggestion:
            yield rc.translate("native.import_error_suggestion.hint", suggestion=self.suggestion)


@KTBException.register
class NameAttributeErrorSuggestHandler(ErrorSuggestHandler, priority=1.1):
    """
    本处理器模仿原生的NameError的拼写错误检测
    为NameError的拼写错误添加额外的正确拼写提示
    并为存在于标准库和第三方库中的名字添加额外的提示
    """

    def __init__(self, exc_type, exc_value, exc_traceback, *, limit=None,
                 lookup_lines=True, capture_locals=False, compact=False,
                 max_group_width=15, max_group_depth=10, _seen=None):
        super().__init__(exc_type, exc_value, exc_traceback)

        self._can_handle = (issubclass(exc_type, (NameError, AttributeError)) and
                            getattr(exc_value, "name", None) is not None)

        if self._can_handle:
            self.wrong_name = getattr(exc_value, "name")
            self.suggestion = compute_suggestion_error(exc_value, exc_traceback, self.wrong_name)
            self.is_stdlib = self.wrong_name in sys.stdlib_module_names

            self.is_3rd_party = False
            import importlib.metadata
            try:
                importlib.metadata.distribution(self.wrong_name)
                self.is_3rd_party = True
            except importlib.metadata.PackageNotFoundError:
                pass

            self.is_lib = self.is_stdlib or self.is_3rd_party

    def can_handle(self, ktb_exc) -> bool:
        return self._can_handle

    @classmethod
    def translation_keys(cls):
        return {
            "default": {
                "native.nameattr_error_suggestion.typo": "Did you mean '{suggestion}'?",
                "native.nameattr_error_suggestion.forget_import": "You may forget to import '{wrong_name}'",
                "native.nameattr_error_suggestion.or_forget_import": "or you may forget to import '{wrong_name}'",
            },
            "zh_hans": {
                "native.nameattr_error_suggestion.typo": "你是不是想输入'{suggestion}'？",
                "native.nameattr_error_suggestion.forget_import": "你可能忘记导入'{wrong_name}'了",
                "native.nameattr_error_suggestion.or_forget_import": "或者你可能忘记导入'{wrong_name}'了",
            }
        }

    def handle(self, ktb_exc) -> Generator[str, None, None]:
        yield from super().handle(ktb_exc)
        if self.suggestion:
            yield rc.translate("native.nameattr_error_suggestion.typo", suggestion=self.suggestion)

        if issubclass(ktb_exc.exc_type, NameError) and self.is_stdlib:
            if self.suggestion:
                yield rc.translate("native.nameattr_error_suggestion.or_forget_import", wrong_name=self.wrong_name)
            else:
                yield rc.translate("native.nameattr_error_suggestion.forget_import", wrong_name=self.wrong_name)

# 以上是所有原生处理中含有新增的处理逻辑的处理器。优先级均为1.1。

"""
BaseException
 ├── SystemExit - TODO
 ├── KeyboardInterrupt - TODO
 ├── GeneratorExit - 不要设计，因为这个异常不会被显示
 ├── Exception - TODO
      ├── StopIteration - StopIterationHandler(ErrorSuggestHandler, priority=1.0)
      ├── StopAsyncIteration - TODO
      ├── ArithmeticError - TODO
      │    ├── FloatingPointError - 简单设计即可，因为这个异常应当不再出现。
      │    ├── OverflowError - OverflowErrorHandler(ErrorSuggestHandler, priority=1.0)
      │    └── ZeroDivisionError - TODO
      ├── AssertionError - TODO
      ├── AttributeError - TODO
      ├── BufferError - TODO
      ├── EOFError - TODO
      ├── ImportError - TODO
      │    └── ModuleNotFoundError - TODO
      ├── LookupError - TODO
      │    ├── IndexError - TODO
      │    └── KeyError - TODO
      ├── MemoryError - TODO
      ├── NameError - TODO
      │    └── UnboundLocalError - TODO
      ├── OSError - TODO
      │    ├── BlockingIOError - TODO
      │    ├── ChildProcessError - TODO
      │    ├── ConnectionError - TODO
      │    │    ├── BrokenPipeError - TODO
      │    │    ├── ConnectionAbortedError - TODO
      │    │    ├── ConnectionRefusedError - TODO
      │    │    └── ConnectionResetError - TODO
      │    ├── FileExistsError - TODO
      │    ├── FileNotFoundError - TODO
      │    ├── InterruptedError - TODO
      │    ├── IsADirectoryError - TODO
      │    ├── NotADirectoryError - TODO
      │    ├── PermissionError - TODO
      │    ├── ProcessLookupError - TODO
      │    └── TimeoutError - TODO
      ├── ReferenceError - TODO
      ├── RuntimeError - TODO
      │    ├── NotImplementedError - TODO
      │    └── RecursionError - TODO
      ├── SyntaxError - TODO
      │    └── IndentationError - TODO
      │         └── TabError - TODO
      ├── SystemError - TODO
      ├── TypeError - TODO
      ├── ValueError - TODO
      │    └── UnicodeError - TODO
      │         ├── UnicodeDecodeError - TODO
      │         ├── UnicodeEncodeError - TODO
      │         └── UnicodeTranslateError - TODO
"""

@KTBException.register
class StopIterationHandler(ErrorSuggestHandler, priority=1.0):  # 原生
    """
    StopIteration异常处理器
    ```
>>> def f():
>>>     for i in range(10):
>>>         yield i
>>>     return "Boom!"
>>>
>>> g = f()
>>> while True:
>>>     next(g)

... Traceback (most recent call last):
...   File "main.py", line 139, in <module>
...     next(g)
(-) StopIteration: Boom!

    改为:

(1) [StopIteration] 生成器'g'停止迭代: Boom!
    ```
    """

    def __init__(self, exc_type, exc_value, exc_traceback, **kwargs):
        super().__init__(exc_type, exc_value, exc_traceback, **kwargs)
        self._can_handle = issubclass(exc_type, StopIteration)
        if not self._can_handle:
            return

        # Python 3.7 之后，对于使用return 关键字的生成器，抛出的StopIteration异常会包含 return 的值。
        self.return_value = exc_value.value if hasattr(exc_value, 'value') else None


    def can_handle(self, ktb_exc) -> bool:
        return self._can_handle

    @classmethod
    def translation_keys(cls):
        return {
            "default": {
                "native.stop_iteration.hint": "[StopIteration] Generator '{generator}' stopped iterating.",
                "native.stop_iteration.hint_with_return": "[StopIteration] Generator '{generator}' stopped: {ret}",
            },
            "zh_hans": {
                "native.stop_iteration.hint": "[StopIteration] 生成器'{generator}'停止迭代。",
                "native.stop_iteration.hint_with_return": "[StopIteration] 生成器'{generator}'停止迭代: {ret}",
            }
        }

    def handle(self, ktb_exc) -> Generator[str, None, None]:
        # 从栈帧中获取生成器在代码里的名称
        self.generator = "<Unknown Generator>"
        if len(ktb_exc.stack) > 0:
            exc_frame = ktb_exc.stack[0]
            tree = ast.parse("".join(linecache.getlines(exc_frame.filename)))
            for node in ast.walk(tree):
                # next(g)
                if (
                    isinstance(node, ast.Call) and  # 检查是否是函数调用
                    isinstance(node.func, ast.Name) and  # 检查是否是显式函数名
                    node.func.id == 'next'  # 检查是否是next调用
                ):
                    self.generator = ast.unparse(node.args[0])  # args 必然包含至少一个元素，否则next会抛出的是TypeError
                    break
                # g.__next__()
                if (
                    isinstance(node, ast.Call) and  # 检查是否是函数调用
                    isinstance(node.func, ast.Attribute) and  # 检查是否是属性访问
                    isinstance(node.func.value, ast.Name) and  # 检查是否是显式属性访问
                    node.func.attr == '__next__'  # 检查是否是__next__方法调用
                ):
                    self.generator = ast.unparse(node.func.value)  # 获取属性访问的对象
                    break

        if self.return_value is not None:
            yield rc.translate("native.stop_iteration.hint_with_return", generator=self.generator, ret=self.return_value)
        else:
            yield rc.translate("native.stop_iteration.hint", generator=self.generator)


@KTBException.register
class StopAsyncIterationHandler(ErrorSuggestHandler, priority=1.0):  # 原生
    """
    StopAsyncIteration异常处理器
    ```
>>> async def f():
>>>     for i in range(10):
>>>         yield i
>>>     return "Boom!"
>>>
>>> async for i in f():
>>>     pass

... Traceback (most recent call last):
...   File "main.py", line 139, in <module>
...     async for i in f():
(-) StopAsyncIteration: Boom!

    改为:

(1) [StopAsyncIteration] 异步生成器'f'停止迭代: Boom!
    ```
    """

    def __init__(self, exc_type, exc_value, exc_traceback, **kwargs):
        super().__init__(exc_type, exc_value, exc_traceback, **kwargs)
        self._can_handle = issubclass(exc_type, StopAsyncIteration)
        if not self._can_handle:
            return

        self.return_value = exc_value.value if hasattr(exc_value, 'value') else None

    def can_handle(self, ktb_exc) -> bool:
        return self._can_handle

    @classmethod
    def translation_keys(cls):
        return {
            "default": {
                "native.stop_async_iteration.hint": "[StopAsyncIteration] Async generator '{generator}' stopped iterating.",
                "native.stop_async_iteration.hint_with_return": "[StopAsyncIteration] Async generator '{generator}' stopped: {ret}",
            },
            "zh_hans": {
                "native.stop_async_iteration.hint": "[StopAsyncIteration] 异步生成器'{generator}'停止迭代。",
                "native.stop_async_iteration.hint_with_return": "[StopAsyncIteration] 异步生成器'{generator}'停止迭代: {ret}",
            }
        }

    def handle(self, ktb_exc) -> Generator[str, None, None]:
        self.generator = "<Unknown Async Generator>"
        if len(ktb_exc.stack) > 0:
            exc_frame = ktb_exc.stack[0]
            tree = ast.parse("".join(linecache.getlines(exc_frame.filename)))
            for node in ast.walk(tree):
                # anext(g)
                if (
                    isinstance(node, ast.Call) and  # 检查是否是函数调用
                    isinstance(node.func, ast.Name) and  # 检查是否是显式函数名
                    node.func.id == 'anext'  # 检查是否是anext调用
                ):
                    self.generator = ast.unparse(node.args[0])  # args 必然包含至少一个元素，否则next会抛出的是TypeError
                    break
                # g.__anext__()
                if (
                    isinstance(node, ast.Call) and  # 检查是否是函数调用
                    isinstance(node.func, ast.Attribute) and  # 检查是否是属性访问
                    isinstance(node.func.value, ast.Name) and  # 检查是否是显式属性访问
                    node.func.attr == '__anext__'  # 检查是否是__anext__方法调用
                ):
                    self.generator = ast.unparse(node.func.value)  # 获取属性访问的对象
                    break

        if self.return_value is not None:
            yield rc.translate("native.stop_async_iteration.hint_with_return",
                             generator=self.generator,
                             ret=self.return_value)
        else:
            yield rc.translate("native.stop_async_iteration.hint",
                             generator=self.generator)

@KTBException.register
class OverflowErrorHandler(ErrorSuggestHandler, priority=1.0):
    """
    OverflowError异常处理器
    ```
>>> import math
>>> math.exp(1000)

... Traceback (most recent call last):
...   File "<input>", line 1, in <module>
(-) OverflowError: math range error

    改为:

(1) [OverflowError] 溢出错误: 数学范围错误
    ```
    """

    def __init__(self, exc_type, exc_value, exc_traceback, **kwargs):
        super().__init__(exc_type, exc_value, exc_traceback, **kwargs)
        self._can_handle = issubclass(exc_type, OverflowError)
        self.err_msg_key = {
            "math range error": "native.overflow_error.msg.math_range_error",
        }.get(str(exc_value), exc_value or "native.overflow_error.msg.novalue")  # match None and ""


    def can_handle(self, ktb_exc) -> bool:
        return self._can_handle

    @classmethod
    def translation_keys(cls):
        return {
            "default": {
                "native.overflow_error.hint": "[OverflowError] {msg}",
                "native.overflow_error.msg.novalue": "A value is too large for the given type",
                "native.overflow_error.msg.math_range_error": "math range error",
            },
            "zh_hans": {
                "native.overflow_error.hint": "[OverflowError] {msg}",
                "native.overflow_error.msg.novalue": "数值太大，超出了给定类型的范围",
                "native.overflow_error.msg.math_range_error": "数学范围错误",
            }
        }

    def handle(self, ktb_exc) -> Generator[str, None, None]:
        self.err_msg = rc.translate(self.err_msg_key)
        yield rc.translate("native.overflow_error.hint", msg=str(self.err_msg))
