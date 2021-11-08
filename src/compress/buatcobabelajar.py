import numpy 
from PIL import Image,ImageOps

#matriks = numpy.arange(12).reshape((3,4))

#print(matriks)

#kiri, tengah, kanan = numpy.linalg.svd(matriks)

#print(len(tengah))

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
def kompresgambarori(matriksawal, rasio):
    matrikshasil = numpy.zeros((matriksawal.shape[0], matriksawal.shape[1], matriksawal.shape[2])) #Inisialisasi matriks kosong sebagai hasilnya
    for warna in range(3): 
        kiri, tengah, kanan = numpy.linalg.svd(matriksawal[:,:,warna]) # ini dekomposisi jadi kiri tengah kanan
        #MENCARI DULU ADA BERAPA BANYAK SINGULAR VALUENYA MATRIKS
        i = cariefektif(tengah) 
        k = round((1-rasio/100)*i)
        tengah = numpy.diag(tengah) #biar tengahnya jadi matriks, bukan array berisi singular values
        matrikshasil[:,:,warna] = kiri[:, 0:k] @ tengah[0:k,0:k] @ kanan[0:k,:] #mengalikan kembali matriksnya
    matrikshasil = matrikshasil.astype('uint8') #INI SOALNYA PIL GABISA BACA ELEMEN FLOAT, DICONVERT DULU JADI UNSIGNED
    gambarmerah = Image.fromarray(matrikshasil[:,:,0], mode=None)
    gambarhijau = Image.fromarray(matrikshasil[:,:,1], mode=None)  #INI UNTUK NJADIIN TIAP WARNA DULU JADI GAMBAR
    gambarbiru = Image.fromarray(matrikshasil[:,:,2], mode=None)
    hasilgambar = Image.merge('RGB', (gambarmerah, gambarhijau, gambarbiru)) #MENGGABUNGKAN TIAP WARNA JADI SATU GAMBAR
    return hasilgambar, i , k


gambarawal = Image.open('./transparan.png') # untuk buka gambarnya pake PIL
matriksawal = numpy.array(gambarawal) 
gambarakhir = Image.fromarray(matriksawal, mode= None)

print(matriksawal)
print(gambarawal.mode)
print(gambarakhir.mode)
print(matriksawal.shape)