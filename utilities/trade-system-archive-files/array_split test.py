

import numpy as np

li = []

for i in range(200):
    li.append(i)

x = np.array_split(li, 3) # [array([1, 2, 3, 4]), array([5, 6, 7]), array([ 8,  9, 10])]


print(x[1])


# for i in range(material):

#     if i < groupe_size*1:

#         print(f"{i} is group_A")

#     elif i >= groupe_size*1 and i < groupe_size*2:

#         print(f"{i} is group_B")

#     elif i >= groupe_size*2 and i < groupe_size*3:

#         print(f"{i} is group_C")

#     else:
#         print(f"{i} is group_D")