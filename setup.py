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
    packages=find_packages(include=['kawaiitb', 'kawaiitb.*']),
    package_data={
        'kawaiitb': ['*.json']
    },
    install_requires=[
        'astroid>=3.3.10',
        'pytest>=7.0.0',
        'pytest-asyncio>=0.23.0',
    ],
    tests_require=[
        'pytest>=7.0.0',
        'pytest-asyncio>=0.23.0',
    ],
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