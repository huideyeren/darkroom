#!/usr/bin/env pipenv-shebang

import argparse
import datetime
import glob

import colorcorrect.algorithm as cca
from colorcorrect.util import from_pil, to_pil
import numpy as np
from PIL import Image, ImageOps, ImageEnhance
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
parser.add_argument("-g", "--gamma", help="Set gamma value.", type=float)
parser.add_argument("-l", "--logarithmic", help="Set logarithmic value.", type=float)
parser.add_argument(
    "-t",
    "--tosaka",
    help="Create a high-contrast image like the one Tosaka senior likes. Set the contrast value.",
    type=float,
)

args = parser.parse_args()

now = datetime.datetime.now()
now_s = now.strftime("%Y-%m-%d_%H-%M-%S")

files = glob.glob("./negative/*.jpg")

for i, file in enumerate(files):
    img = Image.open(file)

    if args.negative is True:
        img = ImageOps.invert(img)

    if args.colorautoadjust is True:
        img = to_pil(cca.automatic_color_equalization(from_pil(img)))

    if args.colorstretch is True:
        img = to_pil(cca.stretch(cca.grey_world(from_pil(img))))

    img = np.asarray(img)
    img = img_as_float(img)

    if args.monochrome is True:
        imgL = exposure.adjust_gamma(img, 2.2)
        img_grayL = rgb2gray(imgL)
        img = exposure.adjust_gamma(img_grayL, 1.0 / 2.2)

    if args.gamma is not None:
        imgG = exposure.adjust_gamma(img, args.gamma)
        img = exposure.adjust_gamma(imgG, 1.0 / args.gamma)

    if args.logarithmic is not None:
        img = exposure.adjust_log(img, args.logarithmic)

    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        img = img_as_ubyte(img)

    img = Image.fromarray(img.astype(np.uint8))

    if args.tosaka is not None:
        imgC = ImageEnhance.Contrast(img)
        img = imgC.enhance(args.tosaka)

    img.save(
        "./positive/{0}_{1}.jpg".format(now_s, (i + 1)), quality=100, subsampling=0
    )
    print("{0}/{1} done!".format((i + 1), str(len(files))))

print("All images have been converted!")
