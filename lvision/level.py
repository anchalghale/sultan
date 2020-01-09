''''Module to find summoner level'''
import cv2
from cutils import crop

OFFSET = [22, 12]


def get_summoner_level(img, ocr, coor):
    '''Finds summoner level'''
    img = crop(img, (coor[0]-22, coor[1]-12, 19, 21))
    img = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    return ocr.predict(img)
