import os
from setuptools import setup

from compton_futu import __version__

# Utility function to read the README file.
# Used for the long_description.  It's nice, because now 1) we have a top level
# README file and 2) it's easier to type in the README file than to put a raw
# string in below ...


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


settings = dict(
    name='compton-futu',
    packages=['compton_futu'],
    version=__version__,
    author='kaelzhang',
    author_email='',
    description=('Futu quant'),
    license='MIT',
    keywords='compton-futu',
    url='https://github.com/kaelzhang/compton-futu',
    long_description=read('README.md'),
    long_description_content_type='text/markdown',
    python_requires='>=3.7',
    classifiers=[
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'License :: OSI Approved :: MIT License',
    ]
)

setup(**settings)
