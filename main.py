## ESRGAN Batch Processor ##

import os
from PIL import Image
from itertools import product

def main():
    # Scan images folder
    images = read_images("images")

    for image in images:
        # Split image into chunks
        tiles = split_image_to_tiles(image[1], image[0], os.path.join(os.getcwd(), "processing"), 256)
        
    # move chunks to model
    # run model
    # move output to processing folder
    # move processed chunks to processed folder
    pass

def read_images(dirName):
    images_dir = os.path.join(os.getcwd(), dirName)
    images = [(f, os.path.join(images_dir, f)) for f in os.listdir(images_dir) if os.path.isfile(os.path.join(images_dir, f))]
    return images

def split_image_to_tiles(filename, dir_in, dir_out, d):
    name, ext = os.path.splitext(filename)
    img = Image.open(os.path.join(dir_in, filename))
    w, h = img.size
    
    grid = product(range(0, h-h%d, d), range(0, w-w%d, d))
    for i, j in grid:
        box = (j, i, j+d, i+d)
        out = os.path.join(dir_out, f'{name}_{i}_{j}{ext}')
        img.crop(box).save(out)

if __name__ == '__main__':
    main()