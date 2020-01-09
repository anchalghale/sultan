''''Module to find summoner level'''
import cv2


def get_summoner_level(img, ocr, default=1):
    '''Finds summoner level'''
    try:
        img = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    except cv2.error:
        return default
    return ocr.predict(img)
