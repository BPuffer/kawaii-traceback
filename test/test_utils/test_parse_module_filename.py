import os
from pathlib import Path

import pytest
import kawaiitb
from kawaiitb.utils import parse_module_filename

@pytest.skipif(os.name != 'nt', reason="Windows-specific test")
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
    cwd = Path(r'C:\Users\usr\Desktop\project')
    spp = {
        Path('C:/Program Files/Python312/Lib'),
        Path('C:/Users/usr/Desktop/project/.venv/Lib'),
        Path('C:/Users/usr/Desktop/project/.venv/Lib/site-packages'),

    }
    ENV = type('ENV', (), {
        'cwd': cwd,
        'site_packages_paths': spp,
        'site_packages_paths_which_after_cwd': set(
            [p for p in spp if p.is_relative_to(cwd)]
        )
    })

    for file_path, expected_module, expected_relative_path in test_cases:
        module, relative_path = parse_module_filename(file_path, env=ENV)
        module = module.replace('\\', '/')
        relative_path = relative_path.replace('\\', '/')
        assert module == expected_module, f"Failed for {file_path}: expected module '{expected_module}', got '{module}'"
        assert relative_path == expected_relative_path, f"Failed for {file_path}: expected relative path '{expected_relative_path}', got '{relative_path}'"

@pytest.skipif(os.name != 'posix', reason="Linux-specific test")
def test_parse_module_filename_linux():
    """Test parse_module_filename with various file paths."""
    test_cases = [
        # (input_path, expected_module, expected_relative_path)
        # 系统标准库文件
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

    cwd = Path('/home/user/project')
    spp = {
        Path('/usr/lib/python3.12'),
        Path('/usr/lib/python3.12/site-packages'),
        Path('/home/user/project/.venv/lib/python3.12'),
        Path('/home/user/project/.venv/lib/python3.12/site-packages'),
    }

    class ENV:
        def __init__(self):
            self.cwd = cwd
            self.site_packages_paths = spp
            self.site_packages_paths_which_after_cwd = set(
                [p for p in spp if p.is_relative_to(cwd)]
            )

    env = ENV()

    for file_path, expected_module, expected_relative_path in test_cases:
        module, relative_path = parse_module_filename(file_path, env=env)
        # 统一使用正斜杠，避免Windows路径问题
        module = module.replace('\\', '/')
        relative_path = relative_path.replace('\\', '/')

        assert module == expected_module, (
            f"Failed for {file_path}: expected module '{expected_module}', got '{module}'"
        )
        assert relative_path == expected_relative_path, (
            f"Failed for {file_path}: expected relative_path '{expected_relative_path}', got '{relative_path}'"
        )
