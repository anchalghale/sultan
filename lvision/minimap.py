''' Module to get minimap related data '''
import collections

import cv2
import numpy

from cutils import crop, find_center

from .constants import MINIMAP_AREAS
from .exceptions import NoCharacterInMinimap

MinimapAreas = collections.namedtuple(
    'MinimapAreas',
    'is_base is_lane is_map_divide is_order_side is_platform is_turret nearest_lane is_chaos_side'
)


def get_minimap_areas(analytics, imgs, coor):
    ''' Finds the position of character in the minimap '''
    analytics.start_timer('get_minimap_areas', 'Calcualting minimap areas')
    output = []
    for area in MINIMAP_AREAS:
        try:
            pixel = imgs[area['file_name']][coor]
            output.append(area['mappings'][tuple(pixel)])
        except IndexError:
            output.append(area['mappings'].values()[0])
    output.append(not output[3])
    analytics.end_timer('get_minimap_areas')
    return MinimapAreas(*output)


def get_minimap_coor(analytics, img):
    ''' Finds the position of character in the minimap '''
    analytics.start_timer('get_minimap_coor', 'Finding minimap coordiantes')
    map_ = crop(img, (834, 577, 183, 183))
    img = cv2.inRange(map_, (255, 255, 255), (255, 255, 255))
    kernel = numpy.ones((2, 2), numpy.uint8)
    img = cv2.erode(img, kernel, iterations=1)
    img = cv2.dilate(img, kernel, iterations=1)
    contours, _ = cv2.findContours(img, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    if contours == []:
        raise NoCharacterInMinimap
    box = sorted(contours, key=cv2.contourArea, reverse=True)[0]
    rect = list(cv2.boundingRect(box))
    h, w = img.shape[:2]
    left_gap = rect[0]
    top_gap = rect[1]
    bot_gap = h - rect[1] - rect[3]
    right_gap = w - rect[0] - rect[2]
    if rect[2] < 40:
        if left_gap > right_gap:
            rect[2] = 40
        else:
            rect[0] -= 40 - rect[2]
            rect[2] = 40
    if rect[3] < 31:
        if top_gap > bot_gap:
            rect[3] = 31
        else:
            rect[1] -= 31 - rect[3]
            rect[3] = 31
    coor = find_center(rect)
    analytics.end_timer('get_minimap_coor')
    return coor
