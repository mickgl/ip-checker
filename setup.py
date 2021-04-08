from setuptools import setup, find_packages

VERSION = '1.0'
DESCRIPTION = "Scan connected IP's using GreyNoise API"
LONG_DESCRIPTION = "Scan connected IP's using GreyNoise API"

# Setting up
setup(
    name="ip-checker",
    version=VERSION,
    author="michgl",
    author_email="<michgl33s@gmail.com>",
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
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
    ]
)
