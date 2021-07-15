#!/usr/bin/env pipenv-shebang

import argparse
import datetime
import glob
import os

import colorcorrect.algorithm as cca
from colorcorrect.util import from_pil, to_pil
import numpy as np
from PIL import Image, ImageOps, ImageEnhance

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
parser.add_argument(
    "-t",
    "--tosaka",
    help="Create a high-contrast image like the one Tosaka senior likes. Set the contrast value.",
    type=float,
)

args = parser.parse_args()

now = datetime.datetime.now()
now_s = now.strftime("%Y-%m-%d_%H-%M-%S")

types = ("*.jpg", "*.JPG", "*.jpeg", "*.JPEG", "*.png", "*.PNG")
files_glob = []
for files in types:
    files_glob.extend(
        glob.glob(
            os.path.join(".", "negative", "**", files),
            recursive=True,
        )
    )

for i, file in enumerate(files_glob):
    img = Image.open(file)

    if args.negative is True:
        img = ImageOps.invert(img)

    if args.colorautoadjust is True:
        img = to_pil(cca.automatic_color_equalization(from_pil(img)))

    if args.colorstretch is True:
        img = to_pil(cca.stretch(cca.grey_world(from_pil(img))))

    if img.mode == "RGBA":
        img.load()
        background = Image.new("RGB", img.size, (255, 255, 255))
        background.paste(img, mask=img.split()[3])

    if args.monochrome is True:
        if img.mode == "L" or img.mode == "LA":
            pass

        if img.mode != "RGB":
            img = img.convert("RGB")
        rgb = np.array(img, dtype="float32")

        rgbL = pow(rgb / 255.0, 2.2)
        r, g, b = rgbL[:, :, 0], rgbL[:, :, 1], rgbL[:, :, 2]
        grayL = 0.299 * r + 0.587 * g + 0.114 * b  # BT.601
        gray = pow(grayL, 1.0 / 2.2) * 255

        img = Image.fromarray(gray.astype("uint8"))

    if args.tosaka is not None:
        imgC = ImageEnhance.Contrast(img)
        img = imgC.enhance(args.tosaka)

    img.save(
        "./positive/{0}_{1}.jpg".format(now_s, (i + 1)), quality=100, subsampling=0
    )
    print("{0}/{1} done!".format((i + 1), str(len(files_glob))))

print("All images have been converted!")
