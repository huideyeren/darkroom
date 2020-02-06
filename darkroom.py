import datetime
import glob
from skimage.color import rgb2gray
from skimage import io, img_as_float, img_as_ubyte, util, exposure
import warnings

now = datetime.datetime.now()
now_s = now.strftime('%Y-%m-%d_%H:%M:%S')

files = glob.glob('./negative/*.jpg')

for i, file in enumerate(files):
    img = io.imread(file)
    img = img_as_float(img)
    img_inverted = util.invert(img)
    
    imgL = exposure.adjust_gamma(img_inverted, 2.2)
    img_grayL = rgb2gray(img_inverted)
    img_gray = exposure.adjust_gamma(img_grayL, 1.0/2.2)
    with warnings.catch_warnings():
        warnings.simplefilter('ignore')
        img_gray = img_as_ubyte(img_gray)
    io.imsave(('./positive/{0}_{1}.jpg'.format(now_s, (i + 1))), img_gray, quality=100)
    print('{0}/{1} done!'.format((i + 1), str(len(files))))

print('All images have been converted!')
