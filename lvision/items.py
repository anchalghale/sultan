'''Module to detect summoner items'''
import collections
import cv2

from cutils import crop

Items = collections.namedtuple('Items', 'one two three five six seven')
RECTANGLES = [(596, 709, 12, 12),
              (619, 709, 12, 12),
              (642, 709, 12, 12),
              (596, 731, 12, 12),
              (619, 731, 12, 12),
              (642, 731, 12, 12)]


def get_summoner_items(image, knearest):
    '''Finds summoners items'''
    def prepare(image, rect):
        img = crop(image, rect)
        img = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
        return img
    items = []

    for rect in RECTANGLES:
        img = prepare(image, rect)
        items.append(knearest.predict(img))

    return Items(*items)
