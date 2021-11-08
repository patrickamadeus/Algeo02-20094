from sympy import Matrix, init_printing
import numpy

init_printing()
A = Matrix(2,3,[1,2,3,4,5,6])
print(A)

B = numpy.arange(1,7).reshape((2,3))
print(B)