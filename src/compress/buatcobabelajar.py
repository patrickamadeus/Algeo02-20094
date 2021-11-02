import numpy 
from PIL import Image,ImageOps

#matriks = numpy.arange(12).reshape((3,4))

#print(matriks)

#kiri, tengah, kanan = numpy.linalg.svd(matriks)

#print(len(tengah))

gambarasli = Image.open('./grey.png') # untuk buka gambarnya pake PIL
matrixasli = numpy.array(gambarasli)
print(matrixasli.ndim)