#!/usr/bin/env python
import ast
import logging
import string
import sys
from argparse import ArgumentParser

from pkg_resources import resource_stream

from importformatter import ImportCollector


logging.basicConfig()

parser = ArgumentParser(description='Groups, sorts, and formats import statements.')
parser.add_argument('-a', '--application', dest='applications', nargs='+', default=[])
parser.add_argument('-s', '--stdlib-file', dest='stdlib_files', nargs='+',
    help='File(s) containing additional module names to add to the standard library set.')
options = parser.parse_args()

stdlib = set()

def add_libraries(stream):
    stdlib.update(map(string.strip, stream.readlines()))

add_libraries(resource_stream('importformatter', 'stdlib.txt'))
if options.stdlib_files:
    map(add_libraries, map(file, options.stdlib_files))

visitor = ImportCollector(options.applications, stdlib)
visitor.visit(ast.parse(sys.stdin.read()))
print visitor
