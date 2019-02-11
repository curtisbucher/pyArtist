#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb  5 00:02:55 2019

@author: curtisbucher
"""

import pygame
import math
from numpy import array
import random
import os


def get_next_square(number: int):
    # Returns the next square number after the given number.
    if number == 0:
        return 1
    if not math.sqrt(number).is_integer():
        return (int(math.sqrt(number)) + 1) ** 2
    else:
        return number


def random_palette(seed: str):
    random.seed(seed)
    palette = []
    for x in range(255):
        palette += [
            (
                random.randint(0, 255),
                random.randint(0, 255),
                random.randint(0, 255),
            )
        ]
    return palette


def gen_image_from_file(filename):
    with open(filename, "rb") as d:
        # Opening file and reading data as bytes
        data = d.read()
        # Making the list a square number for a square image
        data += b" " * (get_next_square(len(data)) - len(data))

        # Creating 2d list from data, then a numpy array
        data = [*zip(*[iter(data)] * int(math.sqrt(len(data))))]
        data = array(data)

    # Initiating pygame
    pygame.init()
    screen = pygame.surfarray.make_surface(data)
    screen = pygame.transform.flip(screen, True, False)
    screen = pygame.transform.rotate(screen, 90)
    screen = pygame.transform.scale(screen, (2000, 2000))
    screen.set_palette(random_palette(filename))

    return screen


def recur_gen_image():
    try:
        os.mkdir("./Images")
    except FileExistsError:
        pass
        for dir, subdirs, files in os.walk('..'):
            for file in files:
                if os.path.splitext(file)[-1] == ".py":
                    img = gen_image_from_file(os.path.join(dir, file))
                    filename = os.path.splitext(file)[0] + ".png"
                    filename = os.path.join("./Images", filename)
                    print(filename)
                    pygame.image.save(img, filename)
                    
    subdirs_list = []
    for dir, subdirs, files in os.walk("./Images"):
        for subdir in subdirs:
            subdirs_list += [os.path.join(dir, subdir)]
    for dir in reversed(subdirs_list):
        try:
            os.rmdir(dir)
        except OSError:
            pass


if __name__ == "__main__":
    recur_gen_image()
#    filename = input("Filename: ")
#    img = gen_image_from_file()
#    try:
#        pygame.image.save(img, filename[: filename.index(".")] + ".png")
#    except Exception:
#        pygame.image.save(img, filename + "png")
