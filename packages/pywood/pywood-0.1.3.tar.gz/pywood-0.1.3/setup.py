from codecs import open
from distutils.core import setup

import setuptools

__title__ = 'pywood'
__description__ = 'Lightweight framework to build Telegram bots.'
__url__ = 'https://github.com/pynista/pywood'
__version__ = '0.1.3'
__author__ = 'Dzmitry Maliuzhenets'
__author_email__ = 'dzmitrymaliuzhenets@gmail.com'
__license__ = 'MIT'
__copyright__ = 'Copyright 2020 Dzmitry Maliuzhenets'

with open('README.md', 'r', 'utf-8') as f:
    readme = f.read()


requirements = [
    'prettyprinter',
    'wheel',
    'telegrambotapiwrapper'
]

setup(
    python_requires='~=3.7',
    name=__title__,
    version=__version__,
    author=__author__,
    author_email=__author_email__,
    description=__description__,
    long_description=readme,
    long_description_content_type='text/markdown',
    url=__url__,
    install_requires=requirements,
    packages=setuptools.find_packages(),
    setup_requires=['wheel'],
    keywords='telegram api bot framework durov',
    classifiers=[

        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Natural Language :: Russian',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: Implementation :: CPython',
        'Operating System :: OS Independent',
    ],
)
