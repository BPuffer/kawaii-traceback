from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="kawaii-traceback",
    version="0.1.0",
    author="BPuffer",
    author_email="mc-puffer@qq.com",
    description="Cute Python traceback beautifier with multilingual support",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/bpuffer/kawaii-traceback",
    packages=find_packages(include=['kawaiitb', 'kawaiitb.*']),  # 明确包含你的包
    install_requires=[
        'astroid>=3.3.10',  # 仅保留运行时必需依赖
    ],
    extras_require={
        "test": [  # 定义测试依赖，供 `pip install -e .[test]` 使用
            "pytest>=7.0.0",
            "pytest-asyncio>=0.23.0",
        ],
    },
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.10",
    keywords='traceback debug error-handling',
)