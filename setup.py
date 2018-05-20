import codecs

from setuptools import setup

from trythatagain import __version__

long_description = codecs.open('README.md', 'r', 'utf8').read()

setup(
    name='trythatagain',
    version=__version__,
    packages=['trythatagain'],
    url='https://github.com/angstwad/trythatagain',
    license='LGPL',
    author='Paul Durivage',
    author_email='pauldurivage@gmail.com',
    description='Decorators for functions that you wish to retry',
    long_description=long_description,
    long_description_content_type='text/markdown',
    extras_require={
        'test': [
            'pytest',
            'pytest-mock',
            'flake8',
        ]
    },
    classifiers=[
        'Topic :: Utilities',
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)',
    ],
)
