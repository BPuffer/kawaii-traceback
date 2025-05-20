import os
import sys
import warnings
from functools import wraps
from traceback import format_exception as orig_format_exception, TracebackException
import kawaiitb.kraceback as traceback
from kawaiitb.config import rc, load_config
from kawaiitb.kraceback import KTBException
from kawaiitb.utils.fromtraceback import parse_value_tb, sentinel as _sentinel

from kawaiitb.kwihandler import ErrorSuggestHandler, SyntaxErrorHandler

__all__ = [
    "traceback",
    "hijack",
    "load",
    "rc",
    "ErrorSuggestHandler",
]

__excepthook__ = sys.excepthook
__in_console__ = hasattr(sys, 'ps1')
if __in_console__:
    __ps1__ = sys.ps1
    __ps2__ = sys.ps2


def unload():
    sys.excepthook = __excepthook__
    if __in_console__:
        sys.ps1 = __ps1__
        sys.ps2 = __ps2__


def hijack(excepthook=True, console_prompt=None):
    if excepthook:
        @wraps(orig_format_exception)  # 签名对齐 traceback.format_exception
        def wrapped(exc, /, value=_sentinel, tb=_sentinel, limit=None, chain=True):
            try:
                value, tb = parse_value_tb(exc, value, tb)
                te = KTBException(type(value), value, tb, limit=limit, compact=True)
                return list(te.format(chain=chain))
            except Exception as e:
                return orig_format_exception(exc, value=_sentinel, tb=_sentinel, limit=None, chain=True) + [
                    "\n\nKawaiiTB occurred another exception while formatting this exception:\n"
                ] + list(TracebackException.from_exception(e).format()) + [
                    "Please report this issue to the developer of KawaiiTB."
                ]

        # 劫持异常处理
        sys.excepthook = lambda etype, value, tb: sys.stderr.write(''.join(wrapped(etype, value, tb)))

    if (console_prompt == True or console_prompt is None) and __in_console__:
        # 劫持控制台提示符
        sys.ps1 = rc.translate("config.prompt1")
        sys.ps2 = rc.translate("config.prompt2")

    if console_prompt == True and not __in_console__:  # 必须显式声明为True
        warnings.warn("[KawaiiTB] Console prompt hijacking is not supported in this environment.")


def load(file=None, lang=None, excepthook=True, console_prompt=True):
    """
    加载配置并劫持hook.

    Args:
        file (file-like | str, optional): 配置文件对象. 如果为None, 则尝试从默认文件加载.
        lang (str, optional): 要加载的语言. 如果为None, 则尝试从配置文件加载.
        excepthook (bool, optional): 是否劫持sys.excepthook. 默认值为True.
        console_prompt (bool, optional): 是否劫持控制台提示符. 默认值为True.
    """
    # 用法: load()
    # 加载默认配置
    if file is None and lang is None:
        load_config()
        return

    # 用法: load("lang")
    # 加载某个默认配置的语言
    if isinstance(file, str) and lang is None:
        lang = file
        file = None

        load_config()
        rc.change_language(lang)

    # 用法: load(open("cfg.json")) | load(file=open("cfg.json"))
    # 加载一个配置文件
    elif hasattr(file, 'readable') and file.readable() and lang is not None:
        try:
            load_config(file)
        except Exception as e:
            raise ValueError(f"Invalid config file") from e

    elif file is not None:
        raise ValueError(f"Invalid type of file {type(file)}")

    # 用法: load(lang="zh_hans")
    elif lang is not None:
        load_config()
        rc.change_language(lang)

    elif file is not None:
        load_config(file)

    hijack(excepthook=excepthook, console_prompt=console_prompt)
