import os
from pathlib import PureWindowsPath, PurePosixPath

import pytest
import kawaiitb
from kawaiitb.utils import parse_filename_sp_namespace

@pytest.mark.skipif(os.name != 'nt', reason="Windows-specific test")
def test_parse_module_filename_win():
    """Test parse_module_filename with various file paths."""
    test_cases = [
        # (input_path, expected_module, expected_relative_path)
        (r"C:\Program Files\Python312\Lib\base64.py", "base64", "base64.py"),
        (r"C:\Program Files\Python312\Lib\site-packages\numpy\random\mtrand.pyx", "numpy", r"numpy/random/mtrand.pyx"),
        (r"C:\Users\usr\Desktop\project\.venv\Lib\base64.py", "base64", "base64.py"),
        (r"C:\Users\usr\Desktop\project\.venv\Lib\site-packages\numpy\random\mtrand.pyx", "numpy", r"numpy/random/mtrand.pyx"),
        (r"C:\Users\usr\Desktop\project\test\test_exc_from_libs.py", ".", r"test/test_exc_from_libs.py"),
        (r"C:\Program Files\Python312\Lib\asyncio\runners.py", "asyncio", r"asyncio/runners.py"),
        (r"C:\Program Files\Python312\Lib\asyncio\base_events.py", "asyncio", r"asyncio/base_events.py"),
        (r"C:\Users\usr\Desktop\project\test\aa\t12.py", ".", r"test/aa/t12.py"),
        (r"C:\Program Files\Python312\Lib\traceback.py", "traceback", "traceback.py"),
    ]
    cwd = PureWindowsPath(r'C:\Users\usr\Desktop\project')
    spp = {
        PureWindowsPath('C:/Program Files/Python312/Lib'),
        PureWindowsPath('C:/Users/usr/Desktop/project/.venv/Lib'),
        PureWindowsPath('C:/Users/usr/Desktop/project/.venv/Lib/site-packages'),

    }
    class ENV:
        def __init__(self):
            self.cwd = cwd
            self.site_packages_paths = spp
            self.site_packages_paths_which_after_cwd = set(
                [p for p in spp if p.is_relative_to(cwd)]
            )
        def get_invalid_site_packages_paths(self):
            return kawaiitb.kraceback._ENV().get_invalid_site_packages_paths()
    env = ENV()

    for file_path, expected_module, expected_relative_path in test_cases:
        module, relative_path = parse_filename_sp_namespace(file_path, env=env)
        # 统一使用正斜杠，方便测试
        module = module.replace('\\', '/')
        relative_path = relative_path.replace('\\', '/')
        assert module == expected_module, f"Failed for {file_path}: expected module '{expected_module}', got '{module}'"
        assert relative_path == expected_relative_path, f"Failed for {file_path}: expected relative path '{expected_relative_path}', got '{relative_path}'"

def test_parse_module_filename_linux():
    """Test parse_module_filename with various file paths."""
    test_cases = [
        # (input_path, expected_module, expected_relative_path)
        ("/usr/lib/python3.12/base64.py", "base64", "base64.py"),
        ("/usr/lib/python3.12/json/__init__.py", "json", "json/__init__.py"),
        ("/usr/lib/python3.12/asyncio/runners.py", "asyncio", "asyncio/runners.py"),
        ("/usr/lib/python3.12/asyncio/base_events.py", "asyncio", "asyncio/base_events.py"),
        ("/usr/lib/python3.12/traceback.py", "traceback", "traceback.py"),
        ("/usr/lib/python3.12/site-packages/numpy/random/mtrand.py", "numpy", "numpy/random/mtrand.py"),
        ("/usr/lib/python3.12/site-packages/requests/__init__.py", "requests", "requests/__init__.py"),
        ("/home/user/project/.venv/lib/python3.12/base64.py", "base64", "base64.py"),
        ("/home/user/project/.venv/lib/python3.12/site-packages/numpy/random/mtrand.py", "numpy",
         "numpy/random/mtrand.py"),
        ("/home/user/project/.venv/lib/python3.12/site-packages/pandas/__init__.py", "pandas", "pandas/__init__.py"),
        ("/home/user/project/test/test_exc_from_libs.py", ".", "test/test_exc_from_libs.py"),
        ("/home/user/project/test/aa/t12.py", ".", "test/aa/t12.py"),
        ("/home/user/project/src/utils.py", ".", "src/utils.py"),
        ("/home/user/project/main.py", ".", "main.py"),
        ("/home/user/project/.venv/lib/python3.12/site-packages/base64.py", "base64", "base64.py"),
        ("/home/user/project/.venv/lib/python3.12/site-packages/some_pkg.py", "some_pkg", "some_pkg.py"),
    ]

    cwd = PurePosixPath('/home/user/project')
    spp = {
        PurePosixPath('/usr/lib/python3.12'),
        PurePosixPath('/usr/lib/python3.12/site-packages'),
        PurePosixPath('/home/user/project/.venv/lib/python3.12'),
        PurePosixPath('/home/user/project/.venv/lib/python3.12/site-packages'),
    }

    class ENV:
        def __init__(self):
            self.cwd = cwd
            self.site_packages_paths = spp
            self.site_packages_paths_which_after_cwd = set(
                [p for p in spp if p.is_relative_to(cwd)]
            )
        def get_invalid_site_packages_paths(self):
            return kawaiitb.kraceback._ENV().get_invalid_site_packages_paths()

    env = ENV()

    for file_path, expected_module, expected_relative_path in test_cases:
        module, relative_path = parse_filename_sp_namespace(file_path, env=env)
        # 统一使用正斜杠，方便测试
        module = module.replace('\\', '/')
        relative_path = relative_path.replace('\\', '/')

        assert module == expected_module, \
            f"Failed for {file_path}: expected module '{expected_module}', got '{module}'"
        assert relative_path == expected_relative_path, \
            f"Failed for {file_path}: expected relative_path '{expected_relative_path}', got '{relative_path}'"

def test_parse_module_filename_qpy():
    test_cases = [
        # (input_path, expected_module, expected_relative_path)
        ("/data/user/0/org.qpython.qpy/files/lib/python3.12/asyncio/base_events.py", "asyncio", "asyncio/base_events.py"),
        ("/data/user/0/org.qpython.qpy/files/lib/python3.12/asyncio/sslproto.py", "asyncio", "asyncio/sslproto.py"),
        ("/data/user/0/org.qpython.qpy/files/lib/python3.12/asyncio/runners.py", "asyncio", "asyncio/runners.py"),
        ("/data/user/0/org.qpython.qpy/files/lib/python3.12/ssl.py", "ssl", "ssl.py"),
        ("/data/user/0/org.qpython.qpy/files/lib/python3.12/traceback.py", "traceback", "traceback.py"),
        ("/data/user/0/org.qpython.qpy/files/lib/python3.12/site-packages/aiohttp/connector.py", "aiohttp", "aiohttp/connector.py"),
        ("/data/user/0/org.qpython.qpy/files/lib/python3.12/site-packages/aiohttp/client.py", "aiohttp", "aiohttp/client.py"),
        ("/storage/emulated/0/main.py", ".", "main.py"),
        ("/storage/emulated/0/project/main.py", ".", "project/main.py"),
        ("/storage/emulated/0/project/path/tmp021.py", ".", "project/path/tmp021.py"),
        ("/storage/emulated/0/project/test/aa/t12.py", ".", "project/test/aa/t12.py"),
    ]

    # QPython 环境的项目根目录（默认用户存储目录）
    cwd = PurePosixPath('/storage/emulated/0')
    # QPython 环境的 site-packages 相关路径集合
    spp = {
        PurePosixPath("/data/user/0/org.qpython.qpy/files/lib/python3.12"),
        PurePosixPath("/data/user/0/org.qpython.qpy/files/lib/python3.12/site-packages"),
    }

    # 模拟 QPython 环境的 ENV 类
    class ENV:
        def __init__(self):
            self.cwd = cwd
            self.site_packages_paths = spp
            self.site_packages_paths_which_after_cwd = set(
                [p for p in spp if p.is_relative_to(cwd)]
            )
        def get_invalid_site_packages_paths(self):
            return kawaiitb.kraceback._ENV().get_invalid_site_packages_paths()

    env = ENV()

    # 执行测试断言
    for file_path, expected_module, expected_relative_path in test_cases:
        module, relative_path = parse_filename_sp_namespace(file_path, env=env)
        # 统一使用正斜杠，方便测试
        module = module.replace('\\', '/')
        relative_path = relative_path.replace('\\', '/')

        assert module == expected_module, (
            f"Failed for QPython path {file_path}: expected module '{expected_module}', got '{module}'"
        )
        assert relative_path == expected_relative_path, (
            f"Failed for QPython path {file_path}: expected relative_path '{expected_relative_path}', got '{relative_path}'"
        )