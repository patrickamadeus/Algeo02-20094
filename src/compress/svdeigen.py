import numpy as np
from numpy.matrixlib.defmatrix import matrix # buat operasi matriks
import sympy as sym # buat bikin matriks yang pake lamda
import random #buat gauss function
# atau from sympy import * ???
# INI BLM DICOBA RUN SAMSEK KARENA SYMNYA ERROR

#KALAU BISA HASILNYA DALAM BENTUK ARRAY
def getEigenValues(matriks):
    row = len(matriks)
    col = len(matriks[0])

    # 1. Bikin matriks lambda
    # bisa juga langsung np.identity(row)
    lamda = sym.symbols('lamda')
    matId = sym.eye(row)
    for i in range (row) :
        for j in range (col) :
            if (j == i):
                #matId[i][j] = lamda
    
    # ini kalo matriks identitas doang blm di lamdain
    #matId = np.zeros((row,col))
    for i in range (row) :
        for j in range (col) :
            if (j == i):
                matId[i][j] = 1
    
    # 2. Mencari fungsi determinan det(lamda.I - A)

    # 3. Mencari persamaan karakteristik -> det = 0

#INI DIPAKENYA NANTI LOOPING SEMUA EIGEN VALUE
def getEigenVector(matriks, eigval):
    # 1. (lamda.I - A)X = 0 

    # 2. Cari hasil persamaan karakteristiknya
        # bisa pake gauss -> bikin matriks augmented dari matriks 1 + insert new columns di paling kanan yang isinya 0 semua

    # 3. Bikin matriks dari hasil persamaan karakteristiknya

def getsvd(matriks):
    ## A. SINGULAR KIRI
    # 1. kali matriks dengan matriks transposenya -> A.A^T
    m = matriks
    mt = m.transpose()
    mnew = np.dot(m, mt)
        # kalo pake numpy -> mnew = np.dot(m, mt)
        # kalo pake sympy -> mnew = m*mt

    # 2. cari eigenvaluesnya A.A^T 
    # ini masih bingung eigenvaluesnya ngumpulinnya gimana dan outputnya apa
    e = [0 for i in range (len(mnew))]
    e = getEigenValues(mnew)

    # 3. cari eigenvectornya A.A^T
    arr = [0 for i in range (len(e))]
    for i in range (len(e)):
        # bikin inisialisasi matriksnya dengan nama matriks arr(i)
        arr[i] = getEigenVector(mnew, e[i])

    # 4. normalisasiin eigenvectornya A.A^T
    norms = [0 for i in range (len(e))]
    for i in range (len(e)) :
        # bikin inisialisasi matriksnya dengan nama matriks norms(i)
        n = np.linalg.matrix(arr[i], axis = 1)
        norms[i] = arr[i]/n
        # dapet matriks U (M X M) dari gabungan eigenvector

    ## B. SINGULAR KANAN
    # 5. kali matriks dengan matriks transposenya -> A^T.A
    mnew2 = np.dot(mt, m)
        # kalo pake numpy -> mnew = np.dot(mt, m)
        # kalo pake sympy -> mnew = mt*m

    # 6. cari eigenvaluesnya A^T.A -> nilai singular = akar dari eigenvaluenya

    # 7. cari eigenvectornya A^T.A

    # 8. normalisasiin eigenvectornya A^T.A
        # dapet matriks V (N X N) dari gabungan eigenvectornya
    
    # 9. transpose matriks V
        # dapet matriks V^T --> fungsinya (nama matriks).np.transpose

    # 10. matriks E = gabungan eigenvalues dari A^T.A

    # 11. A = U x E x V^T
    # return U, E, V^T