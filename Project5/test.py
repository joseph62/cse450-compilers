import sys
from Project5.project import generate_bad_code_from_string
from Project5.project import generate_tree_from_string
from Project5.bad_interpreter import run_bad_code_from_string

source = sys.stdin.read()
output = generate_bad_code_from_string(source)
print(output)
