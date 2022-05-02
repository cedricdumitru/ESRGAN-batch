## ESRGAN Batch Processor ##

import os
from PIL import Image
from itertools import product
import image_slicer
from image_slicer import join
import cv2


def main():
    images = read_images("images")
    for image in images:
        img = image[1]
        num_tiles = 50
        tiles = image_slicer.slice(img, num_tiles, save=False)
        image_slicer.save_tiles(tiles, directory="LR/", prefix="slice")

        os.system("./run_model.sh")

        for tile in tiles:
            tile.filename = tile.filename.replace("LR", "results")
            tile.image = Image.open(tile.filename)

        final = join(tiles)
        final.save('processed/output.png')


def read_images(dirName):
    images_dir = os.path.join(os.getcwd(), dirName)
    images = [(f, os.path.join(images_dir, f)) for f in os.listdir(
        images_dir) if os.path.isfile(os.path.join(images_dir, f))]
    return images


def split_image_to_tiles(filename, dir_in, dir_out, d):
    name, ext = os.path.splitext(filename)
    img = Image.open(os.path.join(dir_in, filename))
    w, h = img.size

    grid = product(range(0, h-h % d, d), range(0, w-w % d, d))
    for i, j in grid:
        box = (j, i, j+d, i+d)
        out = os.path.join(dir_out, f'{name}_{i}_{j}{ext}')
        img.crop(box).save(out)


if __name__ == '__main__':
    main()
