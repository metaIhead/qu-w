from PIL import Image,ImageDraw,ImageOps
import random
import numpy as np
import png

from scipy.misc import imsave
import matplotlib.pyplot as mpl

image_file = Image.open("t.png")
image = image_file.convert('L') # получение монохромного изображения
#image = image_file.convert('1') # convert image to black and white

#обрезать и сохранить изображение
border = (143, 58, 126, 52) # left, up, right, bottom
cpop_image=ImageOps.crop(image, border)
cpop_image.save("res.png", "PNG")

#загрузить значение пикселей иображения
reader = png.Reader(filename='res.png')
w, h, pixels, metadata = reader.read_flat()
#перевести все пиксели в лис
pix=list(pixels)


data=open("data.csv", 'w')
for i in range(len(pix)):
    data.write(str(pix[i])+',')
data.close()

test=open("data.csv", 'r')
test_list=test.readlines()
test.close()

test_str=str(test_list[0])

value_list=test_str.split(',')[:-1]

#перевести строчку со значениями пикселей в форму для  построиние изображения
test_array=(np.asfarray(value_list).reshape(h,w))
#построить изображения по значениям пикселей
mpl.imshow(test_array, cmap="Greys", interpolation='None')
mpl.show()
