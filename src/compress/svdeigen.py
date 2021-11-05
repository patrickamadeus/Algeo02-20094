import numpy as np
import sympy as sm

def getsvd(matriks) :


def getEigen(matriks) :
    row = len(matriks)
    col = len(matriks[0])

    # bikin matriks identitas
    matId = np.zeros((row,col))
    for i in range (row) :
        for j in range (col) :
            if (j == i):
                matId[i][j] = 1