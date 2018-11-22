# coding: utf-8
"""
@author: csy
@license: (C) Copyright 2017-2018
@contact: wyzycao@gmail.com
@time: 2018/11/22 
@desc:
"""

import click


@click.group()
def cli():
    pass


@cli.command()
def runserver(host, port):
    print('runserver')


@cli.command()
@click.option('--coverage', 'coverage', is_flag=True, show_default=True, help='Make a HTML coverage report.')
@click.option('--test_dir', 'test_dir', default='tests', show_default=True,
              help='The directory to discover testcases. Example: tests/test_api.')
def test(coverage, test_dir):
    print('test', coverage, test_dir)


if __name__ == '__main__':
    cli()
