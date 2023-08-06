from setuptools import setup, find_packages
from os.path import join, dirname

__PACKAGE__='pynvg'
__DESCRIPTION__='pynvg is a general purpose library by NVG'
__VERSION__="0.1.0"

setup(
    name=__PACKAGE__,
    version=__VERSION__,
    packages=['pynvg'],
    description=__DESCRIPTION__,
    long_description=open(join(dirname(__file__), 'README.rst')).read(),
    author="lonagi",
    author_email='lonagi22@gmail.com',
    url="https://github.com/lonagi/pynvg",
)