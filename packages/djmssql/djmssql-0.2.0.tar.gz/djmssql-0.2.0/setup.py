#!/usr/bin/env python
"""
Django database backend for firebird
"""
from distutils.core import setup, Command

classifiers = [
    'Development Status :: 3 - Alpha',
    'License :: OSI Approved :: BSD License',
    'Operating System :: OS Independent',
    'Programming Language :: Python',
    'Programming Language :: Python :: 3',
    'Topic :: Database',
    'Framework :: Django',
]

setup(name='djmssql', 
        version='0.2.0',
        description='Django database backend for MS SQLServer',
        long_description=open('README.rst').read(),
        url='https://github.com/nakagami/djmssql/',
        classifiers=classifiers,
        keywords=['Django', 'SQLServer', 'minitds'],
        license='BSD',
        author='Hajime Nakagami',
        author_email='nakagami@gmail.com',
        packages=['djmssql'],
        install_requires=['minitds']
)
