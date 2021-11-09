from PIL import Image
import numpy
import os
import time
# Kalau misal nanti dipakai komentarnya dihapus aja buat baca URL jadi gambar dan sebaliknya
'''import requests 
from io import BytesIO, StringIO
from django.core.files.uploadedfile import InMemoryUploadedFile'''

# BTW INI AKU ASUMSI RASIO (TINGKAT KOMPRESI) ITU PERBANDINGAN SINGULAR_VALUES_DIGUNAKAN / SINGULAR_VALUES_TOTAL YA GAIS
# SOALNYA DI SPEK TUBES TULISANNYA "formatnya dibebaskan, cth: Jumlah singular value yang digunakan"

# KAMUS

# Di spek tubes tu harus PNG atau JPG si? gatau barangkali butuh jadi bikin aja
def convertJPGtoPNG(filename) :
    if filename.endswith('.jpg') :
        awal = Image.open(filename)
        kiri, kanan = os.path.splitext(filename)
        awal.save('{}.png'.format(kiri))
    else :
        print("awalnya bukan jpg")
        
def convertPNGtoJPG(filename) :
    if filename.endswith('.png') :
        awal = Image.open(filename)
        kiri, kanan = os.path.splitext(filename)
        awal.save('{}.jpg'.format(kiri))
    else :
        print("awalnya bukan png")
        
# Terdapat singular values yang sangat kecil sehingga perlu diabaikan
def cariefektif(tengah):
    i = 0
    sudah = False
    while (i < len(tengah) and (not sudah)) : 
        if abs(tengah[i]) >= 1e-8 :
            i += 1
        else :
            sudah = True 
    return i

# TLDR : ini ngambil matriks dari sebuah gambar, pake SVD, singular values dari matriks nya cuman dipake beberapa bergantung rasio
# Trus matriksnya dikaliin lagi, diconvert balik jadi gambar. Trus ngereturn gambar hasil, banyaknya singular values, singular values digunakan
def kompresgambartransparan(matriksawal, rasio):
    matrikshasil = numpy.zeros((matriksawal.shape[0], matriksawal.shape[1], 4)) #Inisialisasi matriks kosong sebagai hasilnya
    for warna in range(3): 
        kiri, tengah, kanan = numpy.linalg.svd(matriksawal[:,:,warna]) # ini dekomposisi jadi kiri tengah kanan
        #MENCARI DULU ADA BERAPA BANYAK SINGULAR VALUENYA MATRIKS
        i = cariefektif(tengah) 
        k = round((1-rasio/100)*i)
        tengah = numpy.diag(tengah) #biar tengahnya jadi matriks, bukan array berisi singular values
        matrikshasil[:,:,warna] = kiri[:, 0:k] @ tengah[0:k,0:k] @ kanan[0:k,:] #mengalikan kembali matriksnya
    matrikshasil[:,:,3] = matriksawal[:,:,3]
    for baris in range(matrikshasil.shape[0]) :
        for kolom in range (matrikshasil.shape[1]):
            if matrikshasil[baris,kolom,3] == 0 :
                matrikshasil[baris,kolom,0] = 0
                matrikshasil[baris,kolom,1] = 0
                matrikshasil[baris,kolom,2] = 0
    matrikshasil = matrikshasil.astype('uint8') #INI SOALNYA PIL GABISA BACA ELEMEN FLOAT, DICONVERT DULU JADI UNSIGNED
    hasilgambar = Image.fromarray(matrikshasil, mode=None)
    return hasilgambar, i , k

def kompresgambar(matriksawal, rasio):
    matrikshasil = numpy.zeros((matriksawal.shape[0], matriksawal.shape[1], 3)) #Inisialisasi matriks kosong sebagai hasilnya
    for warna in range(3): 
        kiri, tengah, kanan = numpy.linalg.svd(matriksawal[:,:,warna]) # ini dekomposisi jadi kiri tengah kanan
        #MENCARI DULU ADA BERAPA BANYAK SINGULAR VALUENYA MATRIKS
        i = cariefektif(tengah) 
        k = round((1-rasio/100)*i)
        tengah = numpy.diag(tengah) #biar tengahnya jadi matriks, bukan array berisi singular values
        matrikshasil[:,:,warna] = kiri[:, 0:k] @ tengah[0:k,0:k] @ kanan[0:k,:] #mengalikan kembali matriksnya
    matrikshasil = matrikshasil.astype('uint8') #INI SOALNYA PIL GABISA BACA ELEMEN FLOAT, DICONVERT DULU JADI UNSIGNED
    hasilgambar = Image.fromarray(matrikshasil, mode=None)
    return hasilgambar, i , k

# Sama seperti kompres gambar transparan, namun versi LA
def kompresgambargreytransparan(matriksawal, rasio):
    matrikshasil = numpy.zeros((matriksawal.shape[0], matriksawal.shape[1], 2)) 
    kiri, tengah, kanan = numpy.linalg.svd(matriksawal[:,:,0]) 
    i = cariefektif(tengah)
    k = round((1-rasio/100)*i)
    tengah = numpy.diag(tengah) 
    matrikshasil[:,:,0] = kiri[:, 0:k] @ tengah[0:k,0:k] @ kanan[0:k,:] 
    matrikshasil[:,:,1] = matriksawal[:,:,1]
    for baris in range(matrikshasil.shape[0]) :
        for kolom in range (matrikshasil.shape[1]):
            if matrikshasil[baris,kolom,1] == 0 :
                matrikshasil[baris,kolom,0] = 0
    matrikshasil = matrikshasil.astype('uint8') 
    hasilgambar = Image.fromarray(matrikshasil[:,:], mode=None)
    return hasilgambar, i , k

# Sama seperti kompres gambar, namun versi L
def kompresgambargrey(matriksawal, rasio):
    matrikshasil = numpy.zeros((matriksawal.shape[0], matriksawal.shape[1])) 
    kiri, tengah, kanan = numpy.linalg.svd(matriksawal[:,:]) 
    i = cariefektif(tengah)
    k = round((1-rasio/100)*i)
    tengah = numpy.diag(tengah) 
    matrikshasil[:,:] = kiri[:, 0:k] @ tengah[0:k,0:k] @ kanan[0:k,:] 
    matrikshasil = matrikshasil.astype('uint8') 
    hasilgambar = Image.fromarray(matrikshasil[:,:], mode= None)
    return hasilgambar, i , k

# ALGORITMA

print("SELAMAT DATANG DI PROGRAM COMPRESSION K32 SARAP")

# KALAU BUKANYA DARI URL :
'''response = requests.get(url)
#gambarawal = Image.open(BytesIO(response.content)) INI CONVERT URL JADI GAMBAR '''
gambarawal = Image.open('./transparan.png')# ini yang secara manual, bisa dihapus nanti
modeawal = gambarawal.mode
modePA = False # UNTUK MENGECEK MODE AWALNYA APAKAH TRANSPARAN P ATAU PA KARENA MEMPROSESNYA BEDA
modeP = False
if gambarawal.mode == 'P' :
    gambarawal = gambarawal.convert('RGBA')
    modeP = True
if gambarawal.mode == 'PA':
    gambarawal = gambarawal.convert('RGBA')
    modePA = True
matriksawal = numpy.array(gambarawal)  # convert gambarnya jadi matriks

rasio = float(input("Masukkan rasio yang anda inginkan (dalam persen): ")) #INPUT RASIO, NANTI DAPET DARI INPUT DI WEBSITE HARUSNYA
waktuawal = time.time()

if (matriksawal.ndim == 3) : 
    if (matriksawal.shape[2] == 3) : # KASUS RGB 
        gambarakhir, banyaksingularvalue, singularvaluedigunakan = kompresgambar(matriksawal, rasio) 
    elif (matriksawal.shape[2] == 2) : # KASUS LA
        gambarakhir, banyaksingularvalue, singularvaluedigunakan = kompresgambargreytransparan(matriksawal, rasio) 
    elif (matriksawal.shape[2] == 4) : # KASUS RGBA 
        gambarakhir, banyaksingularvalue, singularvaluedigunakan = kompresgambartransparan(matriksawal, rasio) 
    if (modeP) :
        gambarakhir = gambarakhir.convert('P')
    if (modePA) :
        gambarakhir = gambarakhir.convert('PA')
elif (matriksawal.ndim == 2) : # KASUS GREYSCALE (L) 
        gambarakhir, banyaksingularvalue, singularvaluedigunakan = kompresgambargrey(matriksawal,rasio)


print("Banyaknya singular values adalah:", banyaksingularvalue)
print("Banyaknya singular values digunakan adalah", singularvaluedigunakan)

gambarakhir.show()
# MENYIMPAN HASILNYA KE file django?
'''hasilIO = StringIO.StringIO()
gambarakhir.save(hasilIO, "PNG")
filehasil = inMemoryUploadedFile(hasilIO, None, 'compressed.png' , hasilIO.len, None)'''

#print(modeawal)
#print(gambarakhir.mode)
#print(gambarawal.size)
#print(gambarakhir.size)

waktuakhir = time.time()
waktueksekusi = waktuakhir - waktuawal
print("Waktu eksekusi program adalah", waktueksekusi)

print('SEKIAN DARI S4R4PP')