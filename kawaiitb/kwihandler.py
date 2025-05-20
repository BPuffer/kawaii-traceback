"""
这里定义错误处理器的基类，动态扩展的示例于此展示。
"""

import sys
from typing import Generator, Any

from kawaiitb import rc
from kawaiitb.kraceback import KTBException
from kawaiitb.utils import format_final_exc_line
from kawaiitb.utils.fromtraceback import (
    compute_suggestion_error, )


@KTBException.register
class ErrorSuggestHandler:
    """
    异常处理器的基类。

    优先级最高的处理器会最先认领异常。
    在KTBException初始化时会顺带初始化所有的处理器。
    在格式化时，KTBException传入自身并判断各处理器是否能处理异常，然后选择优先级最高的处理器。

    优先级原则：
    - 仅ErrorSuggestHandler父类使用0.0优先级。低于此优先级的均不可能认领。
    - 原生级处理器使用1.0优先级。即本文件中的所有附加处理器。
    - 希望官方处理器先认领，认领失败时自己处理时，使用属于(0, 1)的优先级。
    - 希望自己的处理器先认领，认领失败时官方处理器处理时，使用属于(1, +infny)的优先级。
        - 独立的异常类型级别的，使用优先级2。
        - 独立的异常描述级别的，使用优先级3。
        - 针对特定异常参数的建议，使用优先级4。
    """

    priority: float = 0.0  # 优先级，选取多少看处理器的细化程度

    def __init__(self, exc_type, exc_value, exc_traceback, *, limit=None,
                 lookup_lines=True, capture_locals=False, compact=False,
                 max_group_width=15, max_group_depth=10, _seen=None):
        ...
        # 此处可以添加一些初始化逻辑，比如确定自己能不能处理这个异常。
        # 也可以根据这个异常帧的信息处理一些值。
        # 上面传入的东西就是一个异常发生时所有传给你的信息，包括异常的语句，上下文代码，这这那那的。
        # 可以看一些预设的处理器了解一下如何处理这些信息。

        # 另外，如果你是直接继承的ErrorSuggestHandler，其实可以省略super调用，
        # 因为init实际上并没有做什么……

        # 如果也不需要后面的设置，可以用**kwargs来收取所有参数，然后按需提取和忽略。

    def can_handle(self, ktb_exc: KTBException) -> bool:
        """返回本处理器是否能处理异常。"""
        # 处理器接受异常需要满足以下条件：
        # 1. 处理器声明自己能处理异常。
        # 2. 没有更高优先级的处理器能处理异常。
        # 举例来说，ModuleNotFoundErrorHandler和PyyamlNotFoundErrorHandler都能处理`import pyyaml`
        # 但前者只是基本的找不到包提醒，后者则是提供了更详细的解决方案，提示用户应该导入的是yaml。
        # 所以优先级PyyamlNotFoundErrorHandler(4.0) > ModuleNotFoundErrorHandler(2.0)。

        return True  # 基处理器要捕获所有异常

    @classmethod
    def translation_keys(cls) -> dict[str, dict[str, Any]]:
        """
        翻译键。
        每个处理器都可以有自己的翻译键，建议非官方逻辑的处理器使用"exthandler.<namespace>.xxx"命名翻译键。
        返回格式是标准的静态文件格式，即{<language>: {<key>: <value>}}。
        **如果非空，则必须有"default"键**。

        如果你希望单纯翻译一个自定义处理器，你可以定义一个优先级为-1的处理器，然后在其中定义翻译键并注册。
        """
        ...

    def handle(self, ktb_exc: KTBException) -> Generator[str, None, None]:
        """
        处理异常，返回一个生成器，生成器会逐行产生处理后的错误信息。
        并不一定非要每行一定断一下，这只是为了模块的灵活性，如果你需要输出确定不变的多行信息，直接写就是了。

        当然，我永远不推荐直接硬编码。最好先使用translation_keys()来定义翻译键，然后使用rc.translate()来获取翻译。
        毕竟你不知道你的用户会使用什么语言。
        """
        stype: str = ktb_exc.exc_type.__qualname__
        smod: str = ktb_exc.exc_type.__module__
        if smod not in ("__main__", "builtins"):
            if not isinstance(smod, str):
                smod = "<unknown>"
            stype = smod + '.' + stype
        yield format_final_exc_line(stype, ktb_exc.final_exc_str)


@KTBException.register
class SyntaxErrorHandler(ErrorSuggestHandler):
    priority: float = 1.0
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
    def translate_keys(cls):
        return {
            "default": {},
        }

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
                               lineno=self.lineno,)

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
                    caretspace = ((c if c.isspace() else ' ') for c in ltext[:colno])
                    yield '    {}{}'.format("".join(caretspace), ('^' * (end_colno - colno) + "\n"))

        msg = self.msg or "<no detail available>"
        # stype = ktb_exc.exc_type.__qualname__
        # yield "{}: {}{}\n".format(stype, msg, filename_suffix)
        yield from super().handle(ktb_exc)

@KTBException.register
class PyYamlImportErrorHandler(ErrorSuggestHandler):
    priority: float = 4.0

    def __init__(self, exc_type, exc_value, exc_traceback, *, limit=None,
                 lookup_lines=True, capture_locals=False, compact=False,
                 max_group_width=15, max_group_depth=10, _seen=None):
        super().__init__(exc_type, exc_value, exc_traceback)
        
        # 检查是否是pyyaml相关的导入错误
        self._can_handle = (issubclass(exc_type, ImportError) and 
                          getattr(exc_value, "name", "") == "pyyaml")
        
    # 注册扩展翻译键到运行时配置
    @classmethod
    def translation_keys(cls):
        return {
            "default": {
                "exthandler.pyyaml.hint": "Attention: You may have installed the 'pyyaml' package, but you should import 'yaml' instead of 'pyyaml'.\n"
                                          "- Install pyyaml using pip: pip install pyyaml\n"
                                          "- Import yaml in your code: import yaml",
            },
            "zh_hans": {
                "exthandler.pyyaml.hint": "注意：你可能已经安装了pyyaml包，但导入时应该使用'yaml'而不是'pyyaml'。\n"
                                          "- 使用pip安装pyyaml: pip install pyyaml\n"
                                          "- 在代码中导入yaml: import yaml",
            }
        }

    
    def can_handle(self, ktb_exc) -> bool:
        return self._can_handle

    def handle(self, ktb_exc) -> Generator[str, None, None]:
        yield from super().handle(ktb_exc)
        yield rc.translate("exthandler.pyyaml.hint") + "\n"

@KTBException.register
class ImportErrorHandler(ErrorSuggestHandler):
    priority: float = 1.0
    def __init__(self, exc_type, exc_value, exc_traceback, *, limit=None,
                 lookup_lines=True, capture_locals=False, compact=False,
                 max_group_width=15, max_group_depth=10, _seen=None):
        super().__init__(exc_type, exc_value, exc_traceback)

        self._can_handle = issubclass(exc_type, ImportError) and getattr(exc_value, "name_from", None) is not None

        if self._can_handle:
            self.wrong_name = getattr(exc_value, "name_from")
            self.suggestion = compute_suggestion_error(exc_value, exc_traceback, self.wrong_name)


    def can_handle(self, ktb_exc) -> bool:
        return self._can_handle

    def handle(self, ktb_exc) -> Generator[str, None, None]:
        yield from super().handle(ktb_exc)
        if self.suggestion:
            yield f"你是想写'{self.suggestion}'吗?"


@KTBException.register
class NameAttributeErrorHandler(ErrorSuggestHandler):
    priority: float = 1.0

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

    def handle(self, ktb_exc) -> Generator[str, None, None]:
        yield from super().handle(ktb_exc)
        if self.suggestion:
            yield f"你是想写'{self.suggestion}'吗?"

        if issubclass(ktb_exc.exc_type, NameError) and self.is_stdlib:
            if self.suggestion:
                yield f"或者没导入: '{self.wrong_name}'"
            else:
                yield f"猜你没导入: '{self.wrong_name}'"
