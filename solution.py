"""
Rozwiązania do laboratorium 1 z Obrazowania Biomedycznego.
"""
import numpy as np
from obpng import write_png
from obpng import read_png

"""
3 - Kwadrat
"""
def square(size, side, start):
	image = np.zeros((size, size)).astype(np.uint8)
	if ((start[0]+side <= size) & (start[1]+side <= size)):
		image[start[1]:start[1]+side, start[0]:start[0]+side]=255
	else:
		print("Miejsce startowe i wymiary małego kwadratu uniemożliwiają stworzenie rysunku")
	return image

"""
3 - Koło
"""
def midcircle(sizeyx):
	if (sizeyx[0]<sizeyx[1]):
	    size=sizeyx[0]/4
	else:
	    size = sizeyx[1]/4

	size2 = size**2

	image = np.zeros((sizeyx[0], sizeyx[1])).astype(np.uint8)
	for y in range(sizeyx[0]):
	    for x in range(sizeyx[1]):
	        if ((x-(sizeyx[1]/2))**2 + (y-(sizeyx[0]/2))**2 <= size2):
	            image[y, x] = 255

	return image

"""
3 - Szachownica.
"""
def checkerboard(size):
	image = np.zeros((size, size)).astype(np.uint8)
	image[:, :] = 255
	co = size//8

	for j in range(4):
	    for i in range(8):
	            if (i%2==0):
	                image[i*co:i*co+co, j*2*co:j*2*co+co] = 0

	for j in range(4):
	    for i in range(8):
	            if (i%2==1):
	                image[i*co:i*co+co, (j*2+1)*co:(j*2+1)*co+co] = 0


	return image

"""
4 - Interpolacja najbliższych sąsiadów.
"""
def nn_interpolation(source, new_size):
	sizey = source.shape[0]
	sizex = source.shape[1]
	new_sizey = new_size[0]
	new_sizex = new_size[1]
	ratioy = sizey/new_sizey
	ratiox = sizex/new_sizex

	image = np.zeros((new_sizey, new_sizex)).astype(np.uint8)

	for j in range(new_sizex):
		x = round(j*ratiox, 0)
		if x > sizex-1:
			x = sizex-1
		for i in range(new_sizey):
			z = round(i * ratioy, 0)
			if z > sizey-1:
				z = sizey-1
			image[i, j] = source[int(z), int(x)]

	return image

"""
5 - Interpolacja dwuliniowa
"""
def bilinear_interpolation(source, new_size):
	sizey = source.shape[0]
	sizex = source.shape[1]
	new_sizey = new_size[0]
	new_sizex = new_size[1]
	ratioy = sizey/new_sizey
	ratiox = sizex/new_sizex

	image = np.zeros((new_sizey, new_sizex)).astype(np.uint8)

	for j in range(new_sizex):
		xf = j*ratiox
		x = int(xf)
		if x > sizex-2:
			x = sizex-2
		x1 = xf - float(x)
		x2 = float(x)+1- xf

		for i in range(new_sizey):
			zf = i*ratioy
			z = int(zf)
			if z > sizey-2:
				z = sizey-2
			z1 = zf - float(z)
			z2 = float(z)+1 - zf

			value = float(source[z, x])*x2*z2 + float(source[z+1, x])*x2*z1 + float(source[z, x+1])*x1*z2 + float(source[z+1, x+1])*x1*z1
			value = round(value, 0)
			image[i, j] = int(value)

	return image

lenna = read_png('data/mono/lenna.png')
lenna = np.squeeze(lenna)

image = nn_interpolation(lenna, (100, 100))
image = nn_interpolation(image, (512, 512))
write_png(image, 'results/4_nn.png')

image = nn_interpolation(lenna, (100, 100))
image = bilinear_interpolation(image, (512, 512))
write_png(image, 'results/5_bilinear.png')

image = checkerboard(256)
write_png(image, 'results/3_checkerboard.png')

image = midcircle((256, 512))
write_png(image, 'results/2_circle_2.png')

image = square(512, 128, (32, 64))
write_png(image, 'results/1_square.png')


'''size = (4, 4)
image = np.zeros(size).astype(np.uint8)
image[2, 3] = 128
image[1:3, 0:2] = 64
mask = image > 32
img = image[image<32] = 32

print(image)
print(mask)
print(img)

image = np.zeros((128, 128)).astype(np.uint8)
image[1:64, 1:64] = 255

write_png(image, 'foo.png')

image = np.zeros((256, 256)).astype(np.uint8)
for i in range(256):
    image[:, i] = i * 2

write_png(image, 'bar.png')'''
