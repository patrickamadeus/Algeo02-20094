import numpy 

matriks = numpy.arange(24).reshape((2, 4,3))

print(matriks)

kiri, tengah, kanan = numpy.linalg.svd(matriks[:,:,1])

print(kiri)
print(len(tengah))
print(kanan)

i=0
while (i < len(tengah)) :
        if abs(tengah[i]) >= 1e-8 :
            i += 1
        else :
            break #disini sudah didapat banyaknya singular values yakni i
print(i)