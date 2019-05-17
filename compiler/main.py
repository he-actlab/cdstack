#!/usr/bin/env python3
from CMLang.compiler import *

if __name__ == '__main__':
    parse_file('CMLang/tests/simple_example_v2.cm', print_code=True, commented=False)
