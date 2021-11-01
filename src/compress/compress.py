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

# ini buat ngedekomposisi dulu matriksnya jadi kiri tengah kanan 
# trus matriksnya dikompres sampe sebanyak rasio*banyaknya singular values
# trus dikali lagi matriksnya jadi satu kesatuan
def kompresmatriks(matriksawal, rasio):
    matrikshasil = numpy.zeros((matriksawal.shape[0], matriksawal.shape[1], matriksawal.shape[2]))
    for warna in range(3): 
        kiri, tengah, kanan = numpy.linalg.svd(matriksawal[:,:,warna]) # ini dekomposisi jadi kiri tengah kanan
        #MENCARI DULU ADA BERAPA BANYAK SINGULAR VALUENYA MATRIKS
        i = 0
        while (i < len(tengah)) : # KENAPA DICARI DULU? KARENA KADANG KADANG SVD ITU GA AKURAT, MISALNYA HARUSNYA 0 DIA TULIS 10^-16
            if abs(tengah[i]) >= 1e-8 :
                i += 1
            else :
                break #disini sudah didapat banyaknya singular values yakni i
        k = round(rasio*i)
        print(len(tengah))
        print(i) #INI UNTUK NGETES DOANG SI, singular value dari svd dengan yang bener dan dengan yang digunakan
        print(k)
        kirikalitengah = numpy.matmul(kiri[:, 0:k], numpy.diag(tengah)[0:k, 0:k])
        matrikshasil[:,:,warna] = numpy.matmul(kirikalitengah, kanan[0:k, :])
    matrikshasil = matrikshasil.astype('uint8') #INI SOALNYA PIL GABISA BACA ELEMEN FLOAT, DICONVERT DULU JADI UNSIGNED
    return matrikshasil


# ALGORITMA
waktuawal = time.time()

print("SELAMAT DATANG DI PROGRAM COMPRESSION K32 SARAP")

gambarasli = Image.open('../../test/sasugee.png') # untuk buka gambarnya pake PIL

matriksgambar = numpy.array(gambarasli) # convert gambarnya jadi matriks

rasio = float(input("Masukkan rasio yang anda inginkan: ")) #INPUT RASIO, NANTI DAPET DARI INPUT DI WEBSITE HARUSNYA

compressed = kompresmatriks(matriksgambar, rasio) #UNTUK NGEKOMPRES MATRIKS

gambarakhir = Image.fromarray(compressed, mode=None) #CONVERT MATRIKS BALIK JADI IMAGE

gambarakhir.show()

waktuakhir = time.time()
print("Waktu eksekusi program adalah",waktuakhir-waktuawal)

print('SEKIAN DARI S4R4pppp')

