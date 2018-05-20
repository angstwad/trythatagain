from setuptools import setup

from trythatagain import __version__

setup(
    name='trythatagain',
    version=__version__,
    packages=['trythatagain'],
    url='https://github.com/angstwad/trythatagain',
    license='LGPL',
    author='Paul Durivage',
    author_email='pauldurivage@gmail.com',
    description='Decorators for functions that you wish to retry',
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
