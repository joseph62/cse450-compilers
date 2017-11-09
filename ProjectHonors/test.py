#! /usr/bin/env python3

import sys
from ProjectHonors.project import generate_bad_code_from_string
from ProjectHonors.project import generate_tree_from_string
from ProjectHonors.project import generate_output_from_string
from ProjectHonors.bad_interpreter import run_bad_code_from_string

source = sys.stdin.read()
output = generate_output_from_string(source)
print(output)
