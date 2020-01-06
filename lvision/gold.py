# 629, 752, 7, 9
import cv2
from cutils import crop, imshow


def get_gold(img, ocr):
    img = crop(img, (629, 752, 35, 9))
    img = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    gold = ''
    for i in range(5):
        cropped = crop(img, (i * 7, 0, 7, 9))
        gold += str(ocr.predict(cropped))
    return int(gold)
