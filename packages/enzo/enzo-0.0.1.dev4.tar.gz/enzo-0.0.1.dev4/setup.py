import re
from setuptools import setup

with open("src/enzo/__init__.py", encoding="utf8") as f:
    version = re.search(r'__version__ = "(.*?)"', f.read()).group(1)


# Metadata in setup.cfg
setup(
    install_requires=["numpy==1.19.0",], version=version,
)
