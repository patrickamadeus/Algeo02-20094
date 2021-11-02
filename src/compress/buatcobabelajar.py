import numpy 
from PIL import Image

#matriks = numpy.arange(12).reshape((3,4))

#print(matriks)

#kiri, tengah, kanan = numpy.linalg.svd(matriks)

#print(len(tengah))

gambarasli = Image.open('./temp.png') # untuk buka gambarnya pake PIL
matriksgambar = numpy.array(gambarasli) # convert gambarnya jadi matriks
print(matriksgambar[:,:,1])