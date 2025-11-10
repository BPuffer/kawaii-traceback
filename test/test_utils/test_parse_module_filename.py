from pathlib import WindowsPath

import pytest
import kawaiitb
from kawaiitb.utils import parse_module_filename

def test_parse_module_filename():
    """Test parse_module_filename with various file paths."""
    test_cases = [
        # (input_path, expected_module, expected_relative_path)
        (r"C:\Program Files\Python312\Lib\base64.py", "base64", "base64.py"),
        (r"C:\Program Files\Python312\Lib\site-packages\numpy\random\mtrand.pyx", "numpy", r"numpy\random\mtrand.pyx"),
        (r"C:\Users\usr\Desktop\project\.venv\Lib\base64.py", "base64", "base64.py"),
        (r"C:\Users\usr\Desktop\project\.venv\Lib\site-packages\numpy\random\mtrand.pyx", "numpy", r"numpy\random\mtrand.pyx"),
        (r"C:\Users\usr\Desktop\project\test\test_exc_from_libs.py", ".", r"test\test_exc_from_libs.py"),
        (r"C:\Program Files\Python312\Lib\asyncio\runners.py", "asyncio", r"asyncio\runners.py"),
        (r"C:\Program Files\Python312\Lib\asyncio\base_events.py", "asyncio", r"asyncio\base_events.py"),
        (r"C:\Users\usr\Desktop\project\test\aa\t12.py", ".", r"test\aa\t12.py"),
        (r"C:\Program Files\Python312\Lib\traceback.py", "traceback", "traceback.py"),
    ]
    cwd = WindowsPath(r'C:\Users\usr\Desktop\project')
    spp = {
        WindowsPath('C:/Users/usr/Desktop/project/.venv/Lib'),
        WindowsPath('C:/Program Files/Python312/Lib'),
        WindowsPath('C:/Users/usr/Desktop/project/.venv'),
        WindowsPath('C:/Users/usr/Desktop/project/.venv/Lib/site-packages')
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
        assert module == expected_module, f"Failed for {file_path}: expected module '{expected_module}', got '{module}'"
        assert relative_path == expected_relative_path, f"Failed for {file_path}: expected relative path '{expected_relative_path}', got '{relative_path}'"
