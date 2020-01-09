''''Module to find summoner level'''
import cv2
from cutils import crop

OFFSET = [22, 12]


def get_summoner_level(img, ocr):
    '''Finds summoner level'''
    img = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    return ocr.predict(img)
