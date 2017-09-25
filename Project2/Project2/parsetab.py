
# parsetab.py
# This file is automatically generated. Do not edit.
_tabversion = '3.10'

_lr_method = 'LALR'

_lr_signature = "TYPE COMMAND_PRINT COMMAND_RANDOM ID VAL_LITERAL CHAR_LITERAL STRING_LITERAL ASSIGN_ADD ASSIGN_SUB ASSIGN_MULT ASSIGN_DIV COMP_EQU COMP_NEQU COMP_LESS COMP_LTE COMP_GTR COMP_GTE BOOL_AND BOOL_OR WHITESPACE COMMENT UNKNOWN\n    program : statements\n    \n    statements : \n    \n    statements : statements statement\n    \n    statement : expression ';'\n    \n    expression : \n    \n    expression : VAL_LITERAL\n    \n    expression : expression '+' expression\n    \n    expression : expression '-' expression\n    \n    expression : expression '*' expression\n    \n    expression : expression '/' expression\n    "
    
_lr_action_items = {'-':([0,1,3,4,5,6,7,8,9,10,11,12,13,14,],[-2,-5,-3,6,-6,-5,-4,-5,-5,-5,6,6,6,6,]),';':([0,1,3,4,5,6,7,8,9,10,11,12,13,14,],[-2,-5,-3,7,-6,-5,-4,-5,-5,-5,-8,-10,-7,-9,]),'/':([0,1,3,4,5,6,7,8,9,10,11,12,13,14,],[-2,-5,-3,8,-6,-5,-4,-5,-5,-5,8,8,8,8,]),'+':([0,1,3,4,5,6,7,8,9,10,11,12,13,14,],[-2,-5,-3,9,-6,-5,-4,-5,-5,-5,9,9,9,9,]),'VAL_LITERAL':([0,1,3,6,7,8,9,10,],[-2,5,-3,5,-4,5,5,5,]),'$end':([0,1,2,3,7,],[-2,-1,0,-3,-4,]),'*':([0,1,3,4,5,6,7,8,9,10,11,12,13,14,],[-2,-5,-3,10,-6,-5,-4,-5,-5,-5,10,10,10,10,]),}

_lr_action = {}
for _k, _v in _lr_action_items.items():
   for _x,_y in zip(_v[0],_v[1]):
      if not _x in _lr_action:  _lr_action[_x] = {}
      _lr_action[_x][_k] = _y
del _lr_action_items

_lr_goto_items = {'statement':([1,],[3,]),'statements':([0,],[1,]),'expression':([1,6,8,9,10,],[4,11,12,13,14,]),'program':([0,],[2,]),}

_lr_goto = {}
for _k, _v in _lr_goto_items.items():
   for _x, _y in zip(_v[0], _v[1]):
       if not _x in _lr_goto: _lr_goto[_x] = {}
       _lr_goto[_x][_k] = _y
del _lr_goto_items
_lr_productions = [
  ("S' -> program","S'",1,None,None,None),
  ('program -> statements','program',1,'p_program','project.py',122),
  ('statements -> <empty>','statements',0,'p_empty_statements','project.py',128),
  ('statements -> statements statement','statements',2,'p_statements','project.py',134),
  ('statement -> expression ;','statement',2,'p_statement','project.py',141),
  ('expression -> <empty>','expression',0,'p_empty_expression','project.py',148),
  ('expression -> VAL_LITERAL','expression',1,'p_expression_literal','project.py',155),
  ('expression -> expression + expression','expression',3,'p_maths_expression_add','project.py',162),
  ('expression -> expression - expression','expression',3,'p_maths_expression_subtract','project.py',168),
  ('expression -> expression * expression','expression',3,'p_maths_expression_multiply','project.py',175),
  ('expression -> expression / expression','expression',3,'p_maths_expression_divide','project.py',181),
]
