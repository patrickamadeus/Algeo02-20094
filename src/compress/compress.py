### Compress.py ###
# Terdiri atas fungsi-fungsi yang digunakan untuk mengkompres suatu gambar
# Nama pembuat kode :
# 1. Saul Sayers
# 2. Patrick Amadeus Irawan
# 3. Rania Dwi Fadhilah

## Import library ##
from PIL import Image, ImageChops
import numpy
import time
import os
import io
import base64
from io import BytesIO, StringIO
from numpy import random, linalg

# KAMUS
def svd(matriksawal, k):
    # Fungsi SVD menggunakan aproksimasi nilai singular dengan metode power method.
    # Parameter : matriks dan integer
    # Return : matriks U, sigma, dan V transpose

    # Membuat definisi panggilan
    baris = len(matriksawal)
    kolom = len(matriksawal[0])

    # Menginisialisasi matriks hasil dekomposisi svd
    kiri = numpy.zeros((baris, 1))
    tengah = []
    kanan = numpy.zeros((kolom, 1))

    # Mencari nilai matriks untuk sebanyak k awal yang dibutuhkan
    for i in range(k):
        # Men-transpose matriks awal
        matriksawaltranspos = numpy.transpose(matriksawal)

        # Mencari hasil perkalian dot dari transpos matriks awal dengan matriks awal itu sendiri
        matriksgabungan = numpy.dot(matriksawaltranspos, matriksawal)

        # Mencari nilai x
        x = random.normal(0, 1, size=kolom)
        for j in range(10): # pengulangan sebanyak 10 kali untuk memastikan vektor x yang didapat seakurat mungkin
            x = numpy.dot(matriksgabungan, x)
        
        # Mencari nilai distribusi gauss
        normx = numpy.linalg.norm(x)
        v = numpy.divide(x,normx,where=normx!=0)
        
        # mencari nilai singularnya dan menambahkan ke matriks tengah
        nilaisingular = linalg.norm(numpy.dot(matriksawal, v))
        matriksawalv = numpy.dot(matriksawal, v)
        tengah.append(nilaisingular)

        # Mengisi matriks kiri
        u = numpy.reshape(numpy.divide(matriksawalv,nilaisingular,where=nilaisingular!=0), (baris, 1))
        kiri = numpy.concatenate((kiri,u), axis = 1)

        # Mengisi matriks kanan
        v = numpy.reshape(v, (kolom, 1))
        kanan = numpy.concatenate((kanan,v), axis = 1)

        # Mengurangi matriks awal sebelumnya untuk diproses next valuenya
        matriksawal = matriksawal - numpy.dot(numpy.dot(u, numpy.transpose(v)), nilaisingular)
    
    # Mengembalikan kiri,tengah, dan kanan transpose
    return kiri[:, 1:], tengah, numpy.transpose(kanan[:, 1:])

def banyaknyaKdigunakan(matriksawal,rasio):
    # Fungsi untuk menghitung banyaknya k yang akan digunakan
    # Parameter : matriks dan integer
    # Return : integer

    baris, kolom = matriksawal.shape[0], matriksawal.shape[1] 
    if baris < kolom :
        total = baris
    else :
        total = kolom
    digunakan = round((rasio/100)*total)
    return digunakan

def gambartomatriks(gambarawal):
    # Fungsi ini menconvert gambar ke matriks dengan mengecek modeawal terlebih dahulu.
    # Parameter : gambar
    # Return : matriks

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

def matrikstogambar(matrikshasil):  
    # Fungsi ini mengubah matriks ke gambar, diubah ke unsigned int 0 - 255 dahulu sesuai elemen RGB / L
    # Parameter : matriks
    # Return : gambar
     
    numpy.clip(matrikshasil,0,255,matrikshasil)
    matriksunsigned = matrikshasil.astype('uint8') 
    hasilgambar = Image.fromarray(matriksunsigned)
    return hasilgambar

def buangpixelsisa(matrikshasil, berwarna) :
    # Fungsi ini membuat RGB / L nya 0 apabila transparansinya 0 untuk menghemat memori. Parameter boolean berwarna untuk menentukan jenisnya
    # Parameter : matriks dan boolean
    # Return : matriks

    if (berwarna):
        indekstransparansi = 3 #kalau RGBA/CMYK, layer transparansi ada di indeks 3. kalau LA, ada di indeks 1
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

def perubahanpixel(matriksawal,k) : #ALGORITMA DIDAPATKAN DARI QNA FAQ ALGEO NOMOR 6
    baris, kolom = matriksawal.shape[0], matriksawal.shape[1]
    persenselisih = 100*(baris*k + k + kolom*k)/(baris*kolom)
    return persenselisih

# TLDR : ini ngambil matriks dari sebuah gambar, pake SVD, singular values dari matriks nya cuman dipake beberapa bergantung rasio
# Trus matriksnya dikaliin lagi, diconvert balik jadi gambar. Trus ngereturn gambar hasil, banyaknya singular values, singular values digunakan

def kompresgambarwarna(matriksawal, rasio,transparan):
    # Fungsi untuk melakukan kompresi gambar RGB (untuk kasus tidak transparan), RGBA (untuk kasus transparan), CMYK
    # Parameter : matriks, integer, dan boolean
    # Return : gambar

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
    persenselisih = perubahanpixel(matrikshasil,k)
    return hasilgambar, persenselisih

def kompresgambargrey(matriksawal, rasio, transparan):
    # Fungsi untuk melakukan kompresi gambar L (untuk kasus tidak transparan) dan LA (untuk kasus transparan)
    # Parameter : matriks, integer, dan boolean
    # Return : gambar
    k= banyaknyaKdigunakan(matriksawal,rasio)
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
    persenselisih = perubahanpixel(matrikshasil,k)
    return hasilgambar, persenselisih

def selisihbytes(gambarawal, gambarakhir): # MENGECEK PERBEDAANNYA DARI SELISIH BYTES
    bytesawal = io.BytesIO()
    gambarawal.save(bytesawal, 'png')
    bytesakhir = io.BytesIO()
    gambarakhir.save(bytesakhir, 'png')
    #print("ukuran gambar awal adalah", bytesawal.tell(), "bytes")
    #print("ukuran gambar akhir adalah", bytesakhir.tell(), "bytes")
    #print("Persentase perubahan pixel adalah", abs(bytesawal.tell() - bytesakhir.tell())*100/bytesawal.tell(), "persen")
    persenselisih = abs(bytesawal.tell() - bytesakhir.tell())*100/bytesawal.tell()
    return persenselisih

def selisihpixel(gambarawal,gambarakhir): #ALGORITMA DIDAPAT BERDASARKAN SELISIH PIXEL LALU DIBAGI DENGAN MAKSIMAL
    if gambarawal.mode == 'P' or gambarawal.mode == 'PA':
        gambarakhir = gambarakhir.convert('RGBA')
        gambarawal = gambarawal.convert('RGBA')
    selisih = ImageChops.difference(gambarawal, gambarakhir)
    # selisih.show()
    selisihmatrix = numpy.array(selisih)
    if (gambarawal.mode == 'L'):
        persenselisih = selisihmatrix.sum()*100/(selisihmatrix.shape[0]*selisihmatrix.shape[1]*255)
    elif (gambarawal.mode == 'LA' ):
        persenselisih = selisihmatrix[:,:,0].sum()*100/(selisihmatrix.shape[0]*selisihmatrix.shape[1]*255)
    else :
        persenselisih = selisihmatrix[:,:,0:3].sum()*100/(selisihmatrix.shape[0]*selisihmatrix.shape[1]*255*3)
    return persenselisih
    

# ALGORITMA

# print("SELAMAT DATANG DI PROGRAM COMPRESSION K32 SARAP")
def main(gambar,ratio):
    gambarawal = Image.open(gambar)# ini yang secara manual, bisa dihapus nanti
    modeP, modePA, matriksawal = gambartomatriks(gambarawal) # convert gambarnya jadi matriks

    rasio = ratio #INPUT RASIO, NANTI DAPET DARI INPUT DI WEBSITE HARUSNYA
    waktuawal = time.time()

    if (matriksawal.ndim == 3) : 
        if (matriksawal.shape[2] == 3) : # KASUS RGB 
            gambarakhir,persenselisih = kompresgambarwarna(matriksawal, rasio,False) 
        elif (matriksawal.shape[2] == 4) : # KASUS RGBA DAN CMYK
            gambarakhir,persenselisih = kompresgambarwarna(matriksawal, rasio,True) 
        elif (matriksawal.shape[2] == 2) : # KASUS LA
            gambarakhir,persenselisih = kompresgambargrey(matriksawal, rasio, True) 
        if (modeP) :
            gambarakhir = gambarakhir.convert('P') # KASUS P DICONVERT BALIK
        if (modePA) :
            gambarakhir = gambarakhir.convert('PA') # KASUS PA DICONVERT BALIK
    elif (matriksawal.ndim == 2) : # KASUS L 
            gambarakhir,persenselisih = kompresgambargrey(matriksawal,rasio, False)

    #persenselisih = selisihbytes(gambarawal,gambarakhir)
    #persenselisih = selisihpixel(gambarawal, gambarakhir)

    #get base64 img string
    buffered = BytesIO()
    gambarakhir.save(buffered, format=gambarawal.format)
    img_str = base64.b64encode(buffered.getvalue())

    #get Waktu Pemrosesan
    waktuakhir = time.time()
    waktueksekusi = waktuakhir - waktuawal

    return [img_str,waktueksekusi,round(persenselisih,3)]



