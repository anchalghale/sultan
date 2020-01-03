''' Cv2 utility functions '''
import cv2


def coor_offset(coor, offset, size):
    ''' Finds the offset of a coordinate '''
    h, w = size
    y = min(coor[0] + offset[1], h-1)
    x = min(coor[0] + offset[0], w-1)
    return (y, x)


def crop(img, coor, size):
    ''' Crops an cv2 image using coordinate and size '''
    return img[coor[1]:coor[1]+size[1], coor[0]:coor[0]+size[0]]


def find_center(rect):
    ''' Finds the center of the boundingRect value '''
    return (rect[1] + rect[3]//2, rect[0] + rect[2]//2)


def imshow(img):
    ''' Dispalys an image and waits for a key press '''
    cv2.imshow('', img)
    cv2.waitKey()
