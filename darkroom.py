import os
import datetime
import glob
from PIL import Image, ImageOps
import numpy as np

files = glob.glob('./negative/*.jpg')

for file in files:
    img = Image.open(file)
    img = ImageOps.invert(img)
    if img.mode != "RGB":
        img = img.convert("RGB") # any format to RGB
    rgb = np.array(img, dtype="float32");
    rgbL = pow(rgb/255.0, 2.2)
    r, g, b = rgbL[:,:,0], rgbL[:,:,1], rgbL[:,:,2]
    grayL = 0.299 * r + 0.587 * g + 0.114 * b  # BT.601
    gray = pow(grayL, 1.0/2.2)*255
    im_gray = Image.fromarray(gray.astype("uint8"))
    im_gray.save(('./positive/photo_' + str(datetime.datetime.now()) + '.jpg'), quality=100)

print('Done!')
