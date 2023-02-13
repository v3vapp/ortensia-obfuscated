

import ast

ini_list  = '[0,1,2,3,4]'


l = ast.literal_eval(ini_list)

print(type(l))
print(l)

x = max(l)

print(x)