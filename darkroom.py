import os
import datetime
import glob
from PIL import Image, ImageOps

files = glob.glob('./negative/*.jpg')

for file in files:
    img = Image.open(file)
    img_mono = img.convert('L')
    img_invert = ImageOps.invert(img_mono)
    img_invert.save(('./positive/photo_' + str(datetime.datetime.now()) + '.jpg'), quality=100)

print('Done!')
