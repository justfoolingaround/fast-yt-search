from setuptools import find_packages, setup

from ytsearch.__version__ import __version__

setup(
    name="fast-youtube-search",
    version=__version__,
    author="kr@justfoolingaround",
    author_email="kr.justfoolingaround@gmail.com",
    description="The most powerful and fastest YouTube searching Python library.",
    packages=find_packages(),
    url="https://github.com/justfoolingaround/fast-youtube-search",
)
