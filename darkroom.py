#!/usr/bin/env pipenv-shebang

import argparse
import datetime
import glob
from skimage.color import rgb2gray
from skimage import io, img_as_float, img_as_ubyte, util, exposure
import warnings

parser = argparse.ArgumentParser(description='Negative Film Utility')

parser.add_argument(
    '-m',
    '--monochrome',
    help='Convert to monochrome.',
    action='store_true'
)
parser.add_argument(
    '-n',
    '--negative',
    help='Convert negative to positive.',
    action='store_true'
)
parser.add_argument(
    '-g',
    '--gamma',
    help='Set gamma value.',
    type=float
)
parser.add_argument(
    '-l',
    '--logarithmic',
    help='Set logarithmic value.',
    type=float
)

args = parser.parse_args()

now = datetime.datetime.now()
now_s = now.strftime('%Y-%m-%d_%H-%M-%S')

files = glob.glob('./negative/*.jpg')

for i, file in enumerate(files):
    img = io.imread(file)
    img = img_as_float(img)

    if args.negative is True:
        img = util.invert(img)
    
    if args.monochrome is True:
        imgL = exposure.adjust_gamma(img, 2.2)
        img_grayL = rgb2gray(imgL)
        img = exposure.adjust_gamma(img_grayL, 1.0/2.2)

    if args.gamma is not None:
        img = exposure.adjust_gamma(img, args.gamma)
    
    if args.logarithmic is not None:
        img = exposure.adjust_log(img, args.logarithmic)
        
    with warnings.catch_warnings():
        warnings.simplefilter('ignore')
        img = img_as_ubyte(img)

    io.imsave(('./positive/{0}_{1}.jpg'.format(now_s, (i + 1))), img, quality=100)
    print('{0}/{1} done!'.format((i + 1), str(len(files))))

print('All images have been converted!')

