from PIL import Image
import numpy
import os
import time
import base64
from io import BytesIO,StringIO
# Kalau misal nanti dipakai komentarnya dihapus aja buat baca URL jadi gambar dan sebaliknya
'''import requests 
from io import BytesIO, StringIO
from django.core.files.uploadedfile import InMemoryUploadedFile'''

# BTW INI AKU ASUMSI RASIO (TINGKAT KOMPRESI) ITU PERBANDINGAN SINGULAR_VALUES_DIGUNAKAN / SINGULAR_VALUES_TOTAL YA GAIS
# SOALNYA DI SPEK TUBES TULISANNYA "formatnya dibebaskan, cth: Jumlah singular value yang digunakan"

# KAMUS
def eigenvalue(A, v):
    val = A @ v 
    val = numpy.divide(val,v,where=v!=0)
    return val[0]

def svd_dominant_eigen(A, epsilon=0.01):
    """returns dominant eigenvalue and dominant eigenvector of matrix A"""
    n, m = A.shape
    k=min(n,m)
    v = numpy.ones(k) / numpy.sqrt(k)
    if n > m:
        A = A.T @ A
    elif n < m:
        A = A @ A.T
    
    ev = eigenvalue(A, v)

    while True:
        Av = A@ v
        v_new = Av / numpy.linalg.norm(Av)
        ev_new = eigenvalue(A, v_new)
        if numpy.abs(ev - ev_new) < epsilon:
            break

        v = v_new
        ev = ev_new

    return ev_new, v_new

def svd(A, k=None, epsilon=1e-10):
    """returns k dominant eigenvalues and eigenvectors of matrix A"""
    A = numpy.array(A, dtype=float)
    n, m = A.shape
        
    svd_so_far = []
    if k is None:
        k = min(n, m)

    for i in range(k):
        matrix_for_1d = A.copy()

        for singular_value, u, v in svd_so_far[:i]:
            matrix_for_1d -= singular_value * numpy.outer(u, v)

        if n > m:
            _, v = svd_dominant_eigen(matrix_for_1d, epsilon=epsilon)  # next singular vector
            u_unnormalized = A @ v
            sigma = numpy.linalg.norm(u_unnormalized)  # next singular value
            u = u_unnormalized / sigma
        else:
            _, u = svd_dominant_eigen(matrix_for_1d, epsilon=epsilon)  # next singular vector
            v_unnormalized = A.T @ u
            sigma = numpy.linalg.norm(v_unnormalized)  # next singular value
            v = v_unnormalized / sigma

        svd_so_far.append((sigma, u, v))

    singular_values, us, vs = [numpy.array(x) for x in zip(*svd_so_far)]
    return us.T, singular_values, vs

def banyaknyaKdigunakan(matriksawal,rasio):
    baris, kolom = matriksawal.shape[0], matriksawal.shape[1], 
    if baris < kolom :
        total = baris
    else :
        total = kolom
    digunakan = round((1-rasio/100)*total)
    return digunakan

# Fungsi ini menconvert gambar ke matriks dengan mengecek modeawal terlebih dahulu.
def gambartomatriks(gambarawal):
    modePA = False # MENGECEK MODE AWALNYA APAKAH P ATAU PA, KARENA HARUS DICONVERT KE RGBA DULU AGAR AMAN
    modeP = False # KALAU MODE AWALNYA RGB,RGBA,L,LA SUDAH AMAN TERPROSES
    if gambarawal.mode == 'P' :
        gambarawal = gambarawal.convert('RGBA')
        modeP = True
    if gambarawal.mode == 'PA':
        gambarawal = gambarawal.convert('RGBA')
        modePA = True
    matriksawal = numpy.array(gambarawal)  # convert gambarnya jadi matriks
    return modeP, modePA, matriksawal

# Fungsi ini mengubah matriks ke gambar, diubah ke unsigned int 0 - 255 dahulu sesuai elemen RGB / L
def matrikstogambar(matrikshasil):
    matriksunsigned = matrikshasil.astype('uint8') 
    hasilgambar = Image.fromarray(matriksunsigned)
    return hasilgambar

# Fungsi ini membuat RGB / L nya 0 apabila transparansinya 0 untuk menghemat memori. Parameter boolean berwarna untuk menentukan jenisnya
def buangpixelsisa(matrikshasil, berwarna) :
    if (berwarna):
        indekstransparansi = 3 #kalau RGBA, A ada di indeks 3. kalau LA, A ada di indeks 1
    else :
        indekstransparansi = 1
    for baris in range(matrikshasil.shape[0]) :
        for kolom in range (matrikshasil.shape[1]):
            if matrikshasil[baris,kolom,indekstransparansi] == 0 : # APABILA TRANSPARANSINYA 0
                matrikshasil[baris,kolom,0] = 0  # MAKA PIXEL GAMBARNYA JUGA DIBUAT 0
                if (berwarna) :
                    matrikshasil[baris,kolom,1] = 0
                    matrikshasil[baris,kolom,2] = 0
    return matrikshasil


# TLDR : ini ngambil matriks dari sebuah gambar, pake SVD, singular values dari matriks nya cuman dipake beberapa bergantung rasio
# Trus matriksnya dikaliin lagi, diconvert balik jadi gambar. Trus ngereturn gambar hasil, banyaknya singular values, singular values digunakan

# INI UNTUK KOMPRESI VERSI GAMBAR RGB UNTUK TIDAK TRANSPARAN, RGBA UNTUK TRANSPARAN
def kompresgambarwarna(matriksawal, rasio,transparan):
    k= banyaknyaKdigunakan(matriksawal,rasio)
    if (transparan):
        matrikshasil = numpy.zeros((matriksawal.shape[0], matriksawal.shape[1], 4)) #Inisialisasi matriks kosong sebagai hasilnya
    else :
        matrikshasil = numpy.zeros((matriksawal.shape[0], matriksawal.shape[1], 3))
    for warna in range(3): 
        kiri, tengah, kanan = svd(matriksawal[:,:,warna],k) # ini dekomposisi jadi kiri tengah kanan
        tengah = numpy.diag(tengah) #biar tengahnya jadi matriks, bukan array berisi singular values
        matrikshasil[:,:,warna] = kiri[:, 0:k] @ tengah[0:k,0:k] @ kanan[0:k,:] #mengalikan kembali matriksnya
    if (transparan):
        matrikshasil[:,:,3] = matriksawal[:,:,3]
        matrikshasil = buangpixelsisa(matrikshasil,True)
    hasilgambar = matrikstogambar(matrikshasil)
    return hasilgambar

# Sama seperti kompres gambar, tetapi versi L dan LA
def kompresgambargrey(matriksawal, rasio, transparan):
    k= banyaknyaKdigunakan(matriksawal,rasio)
    if (transparan):
        matrikshasil = numpy.zeros((matriksawal.shape[0], matriksawal.shape[1], 2))  #Inisialisasi matriks kosong sebagai hasilnya
        kiri, tengah, kanan = svd(matriksawal[:,:,0], k) 
    else :
        matrikshasil = numpy.zeros((matriksawal.shape[0], matriksawal.shape[1])) 
        kiri, tengah, kanan = svd(matriksawal,k) # ini dekomposisi jadi kiri tengah kanan
    tengah = numpy.diag(tengah) #biar tengahnya jadi matriks, bukan array berisi singular values
    if (transparan) :
        matrikshasil[:,:,0] = kiri[:, 0:k] @ tengah[0:k,0:k] @ kanan[0:k,:] #mengalikan kembali matriksnya kalau transparan
        matrikshasil[:,:,1] = matriksawal[:,:,1]
        matrikshasil = buangpixelsisa(matrikshasil,False)
    else :
        matrikshasil = kiri[:, 0:k] @ tengah[0:k,0:k] @ kanan[0:k,:] #mengalikan kembali matriksnya kalau tidak transparan
    hasilgambar = matrikstogambar(matrikshasil)
    return hasilgambar

# ALGORITMA

# print("SELAMAT DATANG DI PROGRAM COMPRESSION K32 SARAP")

# KALAU BUKANYA DARI URL :
'''response = requests.get(url)
#gambarawal = Image.open(BytesIO(response.content)) INI CONVERT URL JADI GAMBAR '''
gambarawal = Image.open('./binjai.jpeg')# ini yang secara manual, bisa dihapus nanti
print(gambarawal.mode)
modePA = False # UNTUK MENGECEK MODE AWALNYA APAKAH TRANSPARAN P ATAU PA KARENA MEMPROSESNYA BEDA
modeP = False
if gambarawal.mode == 'P' :
    gambarawal = gambarawal.convert('RGBA')
    modeP = True
if gambarawal.mode == 'PA':
    gambarawal = gambarawal.convert('RGBA')
    modePA = True
matriksawal = numpy.array(gambarawal)  # convert gambarnya jadi matriks

rasio = int(input("silahkan input rasio yang diinginkan dalam persen: ")) #INPUT RASIO, NANTI DAPET DARI INPUT DI WEBSITE HARUSNYA
waktuawal = time.time()

if (matriksawal.ndim == 3) : 
    if (matriksawal.shape[2] == 3) : # KASUS RGB 
        gambarakhir = kompresgambarwarna(matriksawal, rasio,False) 
    elif (matriksawal.shape[2] == 4) : # KASUS RGBA 
        gambarakhir = kompresgambarwarna(matriksawal, rasio,True) 
    elif (matriksawal.shape[2] == 2) : # KASUS LA
        gambarakhir = kompresgambargrey(matriksawal, rasio, True) 
    if (modeP) :
        gambarakhir = gambarakhir.convert('P') # KASUS P DICONVERT BALIK
    if (modePA) :
        gambarakhir = gambarakhir.convert('PA') # KASUS PA DICONVERT BALIK
elif (matriksawal.ndim == 2) : # KASUS L 
        gambarakhir = kompresgambargrey(matriksawal,rasio, False)

gambarakhir.show()

waktuakhir = time.time()
waktueksekusi = waktuakhir - waktuawal
print(waktueksekusi)


