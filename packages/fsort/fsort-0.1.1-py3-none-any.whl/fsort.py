"""Cli util to sort large files"""
__version__ = '0.1.1'

import string

from contextlib import ExitStack
from heapq import merge
from itertools import count, islice
from random import choice, randint

import click

chunk_names = []


@click.group()
def cli():
    pass


@cli.command()
@click.option('--filename', help='File to sort')
@click.option('--size', default=50000, help='Size of each chunk')
def external_sort(filename, size):
    """
    Sort file large file by chunks storing these chunks
    into separate files with the given size – 50K by default.

    Result would be `output.txt` file with a sorted text.
    """
    with open(filename) as f:
        for c in count(1):
            sorted_chunk = sorted(islice(f, size))
            if not sorted_chunk:
                break

            chunk_name = f'chunk_{c}.txt'
            chunk_names.append(chunk_name)
            with open(chunk_name, 'w') as chunk_file:
                chunk_file.writelines(sorted_chunk)

    with ExitStack() as stack, open('output.txt', 'w') as of:
        files = (
            stack.enter_context(open(chunk))
            for chunk
            in chunk_names
        )
        of.writelines(merge(*files))


def generate_text(length=None):
    word_length = randint(8, length or 45)
    return ''.join(choice(string.printable) for i in range(length))


@cli.command()
@click.option('--filename', default='large_file.txt', help="File's name")
@click.option('--lines', default=100, help='Rows in a file')
@click.option('--line-length', default=45, help="Max line length")
def create_file(filename, lines, line_length):
    with open(filename, 'w') as f:
        for i in range(lines):
            f.write(f'{generate_text(line_length)}\n')

