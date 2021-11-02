from PIL import Image
import numpy
import os
import time

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

# TLDR : ini ngambil matriks dari sebuah gambar, pake SVD, singular values dari matriks nya cuman dipake beberapa bergantung rasio
# Trus matriksnya dikaliin lagi, diconvert balik jadi gambar. Trus ngereturn gambar hasil, banyaknya singular values, singular values digunakan
def kompresgambar(matriksawal, rasio):
    matrikshasil = numpy.zeros((matriksawal.shape[0], matriksawal.shape[1], matriksawal.shape[2])) #Inisialisasi matriks kosong sebagai hasilnya
    for warna in range(3): 
        kiri, tengah, kanan = numpy.linalg.svd(matriksawal[:,:,warna]) # ini dekomposisi jadi kiri tengah kanan
        #MENCARI DULU ADA BERAPA BANYAK SINGULAR VALUENYA MATRIKS
        i = 0
        sudah = False
        while (i < len(tengah) and (not sudah)) : # KENAPA DICARI DULU? KARENA KADANG KADANG SVD ITU GA AKURAT, MISALNYA HARUSNYA 0 DIA TULIS 10^-16
            if abs(tengah[i]) >= 1e-8 :
                i += 1
            else :
                sudah = True #disini sudah didapat banyaknya singular values yakni i
        k = round((1-rasio/100)*i)
        tengah = numpy.diag(tengah) #biar tengahnya jadi matriks, bukan array berisi singular values
        matrikshasil[:,:,warna] = kiri[:, 0:k] @ tengah[0:k,0:k] @ kanan[0:k,:] #mengalikan kembali matriksnya
    matrikshasil = matrikshasil.astype('uint8') #INI SOALNYA PIL GABISA BACA ELEMEN FLOAT, DICONVERT DULU JADI UNSIGNED
    gambarmerah = Image.fromarray(matrikshasil[:,:,0], mode=None)
    gambarhijau = Image.fromarray(matrikshasil[:,:,1], mode=None)  #INI UNTUK NJADIIN TIAP WARNA DULU JADI GAMBAR
    gambarbiru = Image.fromarray(matrikshasil[:,:,2], mode=None)
    hasilgambar = Image.merge('RGB', (gambarmerah, gambarhijau, gambarbiru)) #MENGGABUNGKAN TIAP WARNA JADI SATU GAMBAR
    return hasilgambar, i , k

def kompresgambargrey(matriksawal, rasio):
    matrikshasil = numpy.zeros((matriksawal.shape[0], matriksawal.shape[1])) 
    kiri, tengah, kanan = numpy.linalg.svd(matriksawal[:,:]) 
    i = 0
    sudah = False
    while (i < len(tengah) and (not sudah)) : 
        if abs(tengah[i]) >= 1e-8 :
            i += 1
        else :
            sudah = True 
    k = round((1-rasio/100)*i)
    tengah = numpy.diag(tengah) 
    matrikshasil[:,:] = kiri[:, 0:k] @ tengah[0:k,0:k] @ kanan[0:k,:] 
    matrikshasil = matrikshasil.astype('uint8') 
    hasilgambar = Image.fromarray(matrikshasil[:,:], mode=None)
    return hasilgambar, i , k


# ALGORITMA

print("SELAMAT DATANG DI PROGRAM COMPRESSION K32 SARAP")

gambarawal = Image.open('./grey.png') # untuk buka gambarnya pake PIL
matriksawal = numpy.array(gambarawal)  # convert gambarnya jadi matriks

rasio = float(input("Masukkan rasio yang anda inginkan (dalam persen): ")) #INPUT RASIO, NANTI DAPET DARI INPUT DI WEBSITE HARUSNYA
waktuawal = time.time()

if (matriksawal.ndim == 3) : # INI KALAU KASUS GAMBARNYA BERWARNA
    gambarakhir, banyaksingularvalue, singularvaluedigunakan = kompresgambar(matriksawal, rasio) #UNTUK NGEKOMPRES gambar
elif (matriksawal.ndim == 2) : # INI KALAU KASUS GAMBARNYA GREYSCALE
    gambarakhir, banyaksingularvalue, singularvaluedigunakan = kompresgambargrey(matriksawal, rasio)

print("Banyaknya singular values adalah:", banyaksingularvalue)
print("Banyaknya singular values digunakan adalah", singularvaluedigunakan)

gambarakhir.show()

waktuakhir = time.time()
waktueksekusi = waktuakhir - waktuawal
print("Waktu eksekusi program adalah", waktueksekusi)

print('SEKIAN DARI S4R4PP')