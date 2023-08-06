import sys
import webbrowser
from distutils.core import setup

message = 'You tried to install "tiny_tokenizer". The name of tiny_tokenizer renamed to "konoha"'

argv = lambda x: x in sys.argv

if (argv('install') or  # pip install ..
        (argv('--dist-dir') and argv('bdist_egg'))):  # easy_install
    raise Exception(message)


if argv('bdist_wheel'):  # modern pip install
    raise Exception(message)


setup(
    name='tiny_tokenizer',
    url='https://pypi.org/project/tiny-tokenizer/',
    version='3.2.0',
    maintainer='Makoto Hiramatsu',
    maintainer_email='himkt@klis.tsukuba.ac.jp',
    long_description=message,
)

