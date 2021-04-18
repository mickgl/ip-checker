from setuptools import setup, find_packages

VERSION = '1.2.1'
DESCRIPTION = "Scan connected IP's using GreyNoise API"

with open("README.md", 'r') as fh:
    LONG_DESCRIPTION = fh.read()

# Setting up
setup(
    name="ip-checker",
    version=VERSION,
    author="michgl",
    author_email="<michgl33s@gmail.com>",
    url="https://github.com/mickgl/ip-checker",
    license="MIT License",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    entry_points="""
    [console_scripts]
    ipchecker = ipchecker.ipchecker:main
    """,
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Operating System :: POSIX",
    ]
)
