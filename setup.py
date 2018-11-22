# coding: utf-8
"""
@author: csy
@license: (C) Copyright 2017-2018
@contact: wyzycao@gmail.com
@time: 2018/11/22 
@desc:
python setup.py sdist
pip install dist/orm-0.0.1.tar.gz
"""

from setuptools import setup

setup(
    name='orm-py',
    version='0.0.1',
    description='A lightweight library For ORM',
    url='https://github.com/caoziyao/orm',
    author='csy',
    author_email='wyzycao@gmail.com',
    license='MIT',
    # https://packaging.python.org/tutorials/packaging-projects/
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
    keywords='orm python',
    packages=['orm'],
)
