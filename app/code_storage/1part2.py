# Практическая работа 1 (часть B)
# Задание №9

from math import *

t = 0
s1 = 5

a, b = cos(t) + s1, b=6*t-3*s1

result = ((a**2 + abs(b))**0.5 - 1) / (abs(a) + abs(b))

print("result =", result)