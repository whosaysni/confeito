# coding: utf-8
"""
==========
 Confer
==========

Confer is a configuration loader library.

Python-based software sometimes employs configuration module like config.py
or settings.py which contains one or more setting variables.

Confer is intended to be a small helper to build those settings
on-the-fly from external source: envvars, database or another file on
same/differnet host.

"""
from setuptools import setup
import sys


setup(
    name='confer',
    version='0.1',
    description='A configration loader library',
    long_description=sys.modules['__main__'].__doc__,
    url='https://github.com/whosaysni/confer',
    author='Yasushi Masuda',
    author_email='whosaysni@gmail.com',
    license='MIT',
    platforms='any',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Plugins',
        'Framework :: Sphinx :: Extension',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Software Development',
    ],
    keywords='configuration, settings',
    packages=['confer'],
    package_dir={'confer': 'src/confer'},
    test_suite='test.suite',  # v2.7 load_tests protocol
)
