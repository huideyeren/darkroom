#!/usr/bin/env pipenv-shebang

import argparse
import datetime
import glob

import colorcorrect.algorithm as cca
from colorcorrect.util import from_pil, to_pil
import numpy as np
from PIL import Image, ImageOps
from skimage.color import rgb2gray
from skimage import io, img_as_float, img_as_ubyte, exposure
import warnings

parser = argparse.ArgumentParser(description="Negative Film Utility")

parser.add_argument(
    "-c",
    "--colorautoadjust",
    help="Adjust color by automatic color equalization.",
    action="store_true",
)
parser.add_argument(
    "-s",
    "--colorstretch",
    help="Adjust color by gray world + stretch.",
    action="store_true",
)
parser.add_argument(
    "-m", "--monochrome", help="Convert to monochrome.", action="store_true"
)
parser.add_argument(
    "-n", "--negative", help="Convert negative to positive.", action="store_true"
)
parser.add_argument("-g", "--gamma", help="Set gamma value.", type=float, default=2.2)
parser.add_argument("-f", "--fixgamma", help="Fix by gamma value.", action="store_true")
parser.add_argument("-l", "--logarithmic", help="Set logarithmic value.", type=float)

args = parser.parse_args()

now = datetime.datetime.now()
now_s = now.strftime("%Y-%m-%d_%H-%M-%S")

files = glob.glob("./negative/*.jpg")

for i, file in enumerate(files):
    img = Image.open(file)

    if args.negative is True:
        print("Invert colors.")
        img = ImageOps.invert(img)

    if args.colorautoadjust is True:
        print("Using automatic color equalization.")
        img = to_pil(cca.automatic_color_equalization(from_pil(img)))

    if args.colorstretch is True:
        print("Using gray world color equalization.")
        img = to_pil(cca.stretch(cca.grey_world(from_pil(img))))

    img = np.asarray(img)
    img = img_as_float(img)

    if args.monochrome is True:
        print("Gamma value is %s.", args.gamma)
        imgL = exposure.adjust_gamma(img, args.gamma)
        img_grayL = rgb2gray(imgL)
        img = exposure.adjust_gamma(img_grayL, 1.0 / args.gamma)

    if args.fixgamma is True:
        print("Gamma value is %s.", args.gamma)
        img = exposure.adjust_gamma(img, args.gamma)

    if args.logarithmic is not None:
        print("Logarithmic value is %s.", args.logarithmic)
        img = exposure.adjust_log(img, args.logarithmic)

    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        img = img_as_ubyte(img)

    io.imsave(("./positive/{0}_{1}.jpg".format(now_s, (i + 1))), img, quality=100)
    print("{0}/{1} done!".format((i + 1), str(len(files))))

print("All images have been converted!")
