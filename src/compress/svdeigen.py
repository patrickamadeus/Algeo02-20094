import numpy as np
from numpy.matrixlib.defmatrix import matrix # buat operasi matriks
import math as mp
from random import gauss

def getEigenValues(m):
    row = len(m)
    col = len(m[0])
    eigval = []

    # 1. Membuat atribut class untuk elemen matriks
    class C:
        # Fungsi untuk assign nilai dari elemen
        def __init__(self, i, j, tan = 0):
            self.i = i
            self.j = j
            self.sin = tan / mp.sqrt(1.0 + tan * tan) 
            self.cos = 1.0 / mp.sqrt(1.0 + tan * tan)

    # 2. Melakukan iterasi QR
    # range = jumlah iterasi
    for i in range(100):
    # a. mengimplementasikan iterasi QR --> (A(k+1) = Q^T x A(k) x Q)
    # menginisialisasi list
        newList = []
    # melakukan operasi perkalian dari kiri, menghapus 0 dari kolom j
        for j in range(col):
            for i in range(row - 1, j, -1):
                if abs(m[j][j]) > 1e-8 :
                    tan = m[i][j] / m[j][j]
                    newlist_1 = C(i, j, tan)
                else:
                    s = C(i, j)
                    s.sin = 1.0
                    s.cos = 0.0
                    newlist_1 = s

                for i in range(col):
                    temp = m[newlist_1.j][i] * newlist_1.cos + m[newlist_1.i][i] * newlist_1.sin
                    m[newlist_1.i][i] = m[newlist_1.i][i] * newlist_1.cos - m[newlist_1.j][i] * newlist_1.sin
                    m[newlist_1.j][i] = temp
                newList.append(newlist_1)
        
        for el in newList:
            for i in range(row):
                temp = m[i][el.j] * el.cos + m[i][el.i] * el.sin
                m[i][el.i] = m[i][el.i] * el.cos - m[i][el.j] * el.sin
                m[i][el.j] = temp
    
    # 3. Mengambil matriks yang berada pada diagonal utama (nilai eigen dari matriks)
    for i in range(len(m)):
        for j in range(len(m[0])):
            if (i == j):
                eigval.append(m[i][j])

    # 4. Mengurutkan nilai eigen yang telah didapatkan untuk mempermudah proses perhitungan pada fungsi-fungsi lainnya    
    for i in range(len(eigval)):
        max = eigval[i]
        j = i + 1
        while j < len(eigval) :
            if eigval[j] > max :
                max = eigval[j]
                eigval[j] = eigval[i]
                eigval[i] = max
            j += 1

    return eigval
            
#INI DIPAKENYA NANTI LOOPING SEMUA EIGEN VALUE
def getEigenVector(matriks, eigval):
    # 1. (lamda.I - A)X = 0 

    # 2. Cari hasil persamaan karakteristiknya
        # bisa pake gauss -> bikin matriks augmented dari matriks 1 + insert new columns di paling kanan yang isinya 0 semua

    # 3. Bikin matriks dari hasil persamaan karakteristiknya

#def getSVD(matriks):
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


### TEST CASE UNTUK EIGENVALUES
test = [1.0, -1.0, 0.0, 0.0, -1.0, 1.0, -1.0, 0.0, 0.0, -1.0, 2.0, 0.0, 0.0, 0.0, 0.0, 3.0] # Example from the book
#test = [1.0 , 3.0, 3.0, 1.0]
m = np.array(test).reshape((4, 4))

print("\n --- Built-in ---")
print(np.linalg.eig(m)[0]) # uses _geev LAPACK routines (see references)

print("\n --- QR ITERATION ---")
print(getEigenValues(m))

### TEST CASE UNTUK EIGENVECTOR


### TEST CASE UNTUK SVD