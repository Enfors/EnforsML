#!/usr/bin/env python3

import errno
import os

import cv2

"""
Functions for dividing images into smaller ones.

"""

SAMPLE_IMAGE_PATH="images/2017 DIEVAR  B14593 381X119 3019T 500X.tif"

def demo():

    num_x = 7
    num_y = 5
    
    img = cv2.imread(SAMPLE_IMAGE_PATH)

    img = cv2.resize(img, None, fx=0.75, fy=0.75,
                     interpolation=cv2.INTER_AREA)

    height, width, channels = img.shape
    
    cv2.imshow("Input image", img)
    cv2.waitKey()

    grid = calc_subimage_grid(width, height, num_x=num_x, num_y=num_y, margin=35)

    for square in grid:
        (top_x, top_y, bot_x, bot_y) = square
        cv2.rectangle(img, (top_x, top_y), (bot_x, bot_y),
                      (0, 255, 0), 1)

    cv2.imshow("With grid", img)
    cv2.waitKey()

    (top_x, top_y, bot_x, bot_y) = grid[0]
    
    cropped = img[top_y:bot_y, top_x:bot_x]

    divide_image_and_save(SAMPLE_IMAGE_PATH, num_x, num_y, margin=35)


def divide_image(image_path, num_x, num_y, margin=0):
    """
    Create a grid of num_x columns and num_y rows of an image, and return
    a list of images representing each square in the grid.

    Args:
        image_path (str): The path to the image file.
        num_x (int): The number of columns you want the grid to have.
        num_y (int): The number of rows you want the grid to have.
        margin (int): The number of pixels on each side of the original
                      image that you want to leave out as margin.

    Returns:
        A list of images representing the squares of the grid.
    """
    subimages = list()

    if not os.path.isfile(image_path):
        raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), image_path)
    
    img = cv2.imread(image_path)

    height, width, channels = img.shape

    grid = calc_subimage_grid(width, height, num_x, num_y, margin)

    for square in grid:
        (top_x, top_y, bot_x, bot_y) = square

        subimage = img[top_y:bot_y, top_x:bot_x]
        subimages.append(subimage)

    return subimages


def divide_image_and_save(image_path, num_x, num_y, margin=0):
    """
    Divide an image into num_x colums and num_y rows, and save each part
    in its own file. In most cases, this is the function you want to use.

    Args:
        image_path (str): The path to the file of the original image.
        num_x (int): The number of columns to use.
        num_y (int): The number of rows to use.
        margin (int): How many pixels of margin to use on each side of
                      the original image.

    Returns:
        The number of files saved.
    
    """
    
    subimage_num = 0

    subimages = divide_image(image_path, num_x, num_y, margin)
    dirname = os.path.dirname(image_path)

    for subimage in subimages:
        cv2.imwrite(os.path.join(dirname, "subimage-%04d.png" % (subimage_num + 1)), subimage)
        subimage_num += 1

    return subimage_num


def calc_subimage_grid(image_x_size, image_y_size, num_x, num_y, margin=0):
    """
    Calculate a grid for an image.

    Args:
        image_x_size (int): The width of the image in pixels.
        image_y_size (int): The height of the image in pixels.
        num_x (int): The number of columns you want the grid to have.
        num_y (int): The number of rows you want the grid to have.
        margin (int): How many pixels of margin of the original image
                      you want to leave out of the grid.
    Returns:
        A list of lists where each element represents a subimage:
        ((top_x, top_y, bot_x, bot_y), ...)

    >>> calc_subimage_grid(10, 10, 2, 2)
    [[0, 0, 4, 4], [0, 5, 4, 9], [5, 0, 9, 4], [5, 5, 9, 9]]
    """
    
    
    subimage_params = list()
    
    (sub_x_size, sub_y_size, x_offset, y_offset) = \
        calc_subimage_size(image_x_size, image_y_size,
                           num_x, num_y, margin)

    for x in range(0, num_x):
        for y in range(0, num_y):
            subimage_param = [(x * sub_x_size) + x_offset,
                              (y * sub_y_size) + y_offset,
                              ((x + 1) * sub_x_size) + x_offset - 1,
                              ((y + 1) * sub_y_size) + y_offset - 1]

            subimage_params.append(subimage_param)

    return subimage_params


def calc_subimage_size(image_x_size, image_y_size, num_x, num_y, margin=0):
    """Given an image of size image_x_size by image_y_size pixels,
    calculate how many pixels each subimage would be, if we want to
    divide it into a grid of size num_x by num_y subimages.

    Args:
        image_x_size (int): The width of the original image in pixels.
        image_y_size (int): The width of the original image in pixels.
        num_x (int): The number of columns of subimages you want.
        num_y (int): The number of rows of subimages you want.
        margin (int): The number of pixels of margins around all edges
                      of the original image which should be discounted.

    Returns:
        (sub_x_size, sub_y_size, x_offset, y_offset)
        sub_x_size (int): How many pixels wide each subimage should be.
        sub_y_size (int): How many pixels tall each subimage should be.
        x_offset (int): The offset from the left edge of the original
                        image to the first column of subimages.
        y_offset (int): The offset from the top edge of the original
                        image to the first row of subimages.

    Usage examples:

    Here we say that our original image is 30 by 30 pixels, and we
    want to make a grid of 6 columns and 6 rows, with no margin.
    The function tells us that we will be able to make a grid where
    each subimage is 5 by 5 pixels, and that there is no offset
    (because we didn't specify a margin):

    >>> calc_subimage_size(image_x_size=30, image_y_size=30,
    ...     num_x=6, num_y=6)
    (5, 5, 0, 0)

    Now we have an original image of 30 by 20 pixels, and we want
    to have a grid with 5 columns and 2 rows, and a margin on each
    side of the original image of 2 pixels.

    >>> calc_subimage_size(image_x_size=30, image_y_size=20,
    ...     num_x=5, num_y=2, margin=2)
    (5, 8, 3, 2)

    >>> calc_subimage_size(image_x_size=200, image_y_size=100,
    ...     num_x=10, num_y=5, margin=20)
    (16, 12, 20, 20)
    """


    sub_x_size = int((image_x_size - (margin * 2)) / num_x)
    sub_y_size = int((image_y_size - (margin * 2)) / num_y)

    x_offset = int(((image_x_size - margin) % num_x) / 2) + margin
    y_offset = int(((image_y_size - margin) % num_y) / 2) + margin

    return sub_x_size, sub_y_size, x_offset, y_offset
    

if __name__ == "__main__":
    import doctest

    doctest.testmod()
    demo()
    
