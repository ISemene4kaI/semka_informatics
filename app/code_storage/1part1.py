# Практическая работа 1
# Задание №9

import math

# 1
x = 2
y = 3
expr1 = 4**(x**2) + math.sin(3*x/(7*y))**2 + 0.3

# 2
x = 1
expr2 = math.log(x)**2 - abs(math.cos(x + 3))

# 3
x = 0.3
expr3 = (math.asin(x)**3 + 1 - x) / (3*x)

# 4
x = 2
expr4 = (x**0.5 + (x-1)**1/3 + math.e**(-3*x)) / (x + 3.5 * (x**2))

print("1 =", expr1)
print("2 =", expr2)
print("3 =", expr3)
print("4 =", expr4)