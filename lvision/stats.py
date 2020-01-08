'''Module to find stats'''

import cv2

from cutils import crop


def get_attack_speed(image, ocr):
    '''Finds attack speed'''
    img = crop(image, (244, 740, 5, 6))
    img = cv2.resize(img, (7, 9))
    img = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)

    hundred = ocr.predict(img)

    img = crop(image, (251, 740, 5, 6))
    img = cv2.resize(img, (7, 9))
    img = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)

    tens = ocr.predict(img)

    img = crop(image, (256, 740, 5, 6))
    img = cv2.resize(img, (7, 9))
    img = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)

    ones = ocr.predict(img)
    try:
        return int(str(hundred) + str(tens) + str(ones))/100
    except ValueError:
        return -1
