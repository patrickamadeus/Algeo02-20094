from PIL import Image
import numpy
import os
import time
from numpy import random, linalg
# Kalau misal nanti dipakai komentarnya dihapus aja buat baca URL jadi gambar dan sebaliknya
'''import requests 
from io import BytesIO, StringIO
from django.core.files.uploadedfile import InMemoryUploadedFile'''

# BTW INI AKU ASUMSI RASIO (TINGKAT KOMPRESI) ITU PERBANDINGAN SINGULAR_VALUES_DIGUNAKAN / SINGULAR_VALUES_TOTAL YA GAIS
# SOALNYA DI SPEK TUBES TULISANNYA "formatnya dibebaskan, cth: Jumlah singular value yang digunakan"

# KAMUS
def svd(A, rank, iterations=10):
    # Assign values
    row = len(A)
    col = len(A[0])

    # Initialize matrix
    U = numpy.zeros((row, 1))
    S = []
    V = numpy.zeros((col, 1))

    # Do the SVD using the power method
    for i in range(rank):
        # Assign initial value
        sigma = 1

        # Transpose the A matrix
        AT = numpy.transpose(A)

        # Find the dot product of A transpose & A itself
        B = numpy.dot(AT, A)

        # Assigning the x value
        x = random.normal(0, sigma, size=col)
        for i in range(iterations):
            x = numpy.dot(B, x)
        
        # Find the random distribution
        normx = numpy.linalg.norm(x)
        v = numpy.divide(x,normx,where=normx!=0)
        
        # Assign the sigma value
        sigma = linalg.norm(numpy.dot(A, v))
        Av = numpy.dot(A, v)
        S.append(sigma)

        # Assign the U matrix
        u = numpy.reshape(numpy.divide(Av,sigma,where=sigma!=0), (row, 1))
        U = numpy.hstack((U, u))

        # Assign the V matrix
        v = numpy.reshape(v, (col, 1))
        V = numpy.hstack((V, v))

        # Assigning the new A matrix
        A = A - numpy.dot(numpy.dot(u, numpy.transpose(v)), sigma)
    
    return U[:, 1:], S, numpy.transpose(V[:, 1:])

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
    print("banyaknya singularvalues total adalah", k/(1-rasio/100))
    print("banyaknya singular values digunakan adalah", k)
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
    print("banyaknya singularvalues total adalah", k/(1-rasio/100))
    print("banyaknya singular values digunakan adalah", k)
    if (transparan):
        matrikshasil = numpy.zeros((matriksawal.shape[0], matriksawal.shape[1], 2))  #Inisialisasi matriks kosong sebagai hasilnya
        kiri, tengah, kanan = svd(matriksawal[:,:,0],k) 
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
gambarawal = Image.open('./src/compress/jokowi.jpeg')# ini yang secara manual, bisa dihapus nanti
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