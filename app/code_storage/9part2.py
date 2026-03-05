import numpy as np

A = np.array([[1,5,1],
              [4,-1,1],
              [9,32,84]])

B = np.array([-12,-21,-1859])

X = np.linalg.solve(A,B)
detA = np.linalg.det(A)
A_inv = np.linalg.inv(A)

print(X)
print(detA)
print(A_inv)
