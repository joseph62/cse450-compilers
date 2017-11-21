#! /usr/bin/env python3
import sys
from Project7.project import generate_bad_code_from_string
from Project7.project import generate_ugly_code_from_string
from Project7.project import generate_tree_from_string
from Project7.bad_and_ugly_interpreter import run_bad_code_from_string,run_ugly_code_from_string

source = sys.stdin.read()
output = generate_ugly_code_from_string(source)
#output = generate_bad_code_from_string(source)
print(output)
