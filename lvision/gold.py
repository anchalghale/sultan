# 629, 752, 7, 9
'''Module to get gold'''
import cv2
from cutils import crop


def get_gold(img, knearest):
    '''Finds gold value'''
    img = crop(img, (629, 752, 35, 9))
    img = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    gold = ''
    for i in range(5):
        cropped = crop(img, (i * 7, 0, 7, 9))
        gold += str(knearest['gold'].predict(cropped))
    try:
        return int(gold)
    except ValueError:
        return -1
