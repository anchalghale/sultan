''' Object detection module '''
import cv2
import numpy

from cutils import coor_offset, crop, find_center, get_color_diff, get_nearest

from .abilities import get_level_ups, get_abilities, get_ability_points

from .constants import MINIMAP_AREAS, CAMERA_LOCK, LEVEL_Q, LEVEL_W, LEVEL_E, LEVEL_R
from .exceptions import NoCharacterInMinimap


def get_small_hp_value(hp_img):
    ''' Calcuates the hp of given image of width 60 '''
    try:
        hp_img = hp_img.reshape((60, 3))
    except ValueError:
        return 60
    reference = hp_img[1]
    for i, value in enumerate(hp_img):
        if get_color_diff(reference, value) > 50:
            return i
    return 60


def identify_object(img, coor):
    ''' Indentify an object from the coordiate '''
    size = img.shape[:2]
    output = {'coor': coor}
    colors = (0, 255, 0), (255, 0, 0), (255, 255, 0), (0, 0, 255), (0, 0, 134)
    mappings = dict(zip(colors, ('champion', 'structure', 'monster', 'minion', 'small_monster')))
    nearest_color = get_nearest(img[coor_offset(coor, (0, -1), size)], colors, 25)
    if nearest_color is None:
        return None
    if mappings[nearest_color] == 'champion':
        output['name'] = 'champion'
    elif mappings[nearest_color] == 'structure':
        output['name'] = 'structure'
    elif mappings[nearest_color] == 'monster':
        output['name'] = 'monster'
    elif mappings[nearest_color] == 'small_monster':
        output['name'] = 'small_monster'
    elif mappings[nearest_color] == 'minion':
        color = img[coor_offset(coor, (1, 0), size)]
        colors = (98, 167, 231), (224, 114, 112), (219, 170, 130)
        mappings = dict(zip(colors, ('ally_minion', 'enemy_minion', 'plant')))
        output['name'] = mappings[get_nearest(color, colors)]
        hp_bar = img[coor[1]:coor[1]+1, coor[0]+1:coor[0]+61]
        output['health'] = get_small_hp_value(hp_bar)
        output['center'] = coor[0]+30, coor[1]+35
        output['is_order_side'] = output['center'][1] / \
            output['center'][0] > img.shape[0]/img.shape[1]
        output['is_turret'] = tuple(img[coor_offset(coor, (-1, 0), size)]) == (0, 36, 21)
    return output


def identify_turret(contour, area):
    ''' Indentify an turret from contour '''
    if area > 2000:
        x, y, w, h = cv2.boundingRect(contour)
        center = x + w//2, y + h - 30
        return {'name': 'turret', 'coor': tuple(contour[0][0]), 'center': center}
    return None


def get_objects(analytics, img, start, end):
    ''' Finds the league objects '''
    analytics.start_timer('get_objects', 'Finding objects')
    threshed = cv2.inRange(img, start, end)
    contours, _ = cv2.findContours(
        threshed, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    objects = []
    for contour in contours:
        area = cv2.contourArea(contour)
        turret = identify_turret(contour, area)
        if turret is not None:
            objects.append(turret)
            continue
        if area == 0:
            obj = identify_object(img, tuple(contour[0][0]))
            if obj is not None:
                objects.append(obj)
    analytics.end_timer('get_objects')
    return objects


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


def get_minimap_areas(analytics, imgs, coor):
    ''' Finds the position of character in the minimap '''
    analytics.start_timer('get_minimap_areas', 'Calcualting minimap areas')
    output = {}
    for area in MINIMAP_AREAS:
        pixel = imgs[area['file_name']][coor]
        output[area['name']] = area['mappings'][tuple(pixel)]
    output['is_chaos_side'] = not output['is_order_side']
    analytics.end_timer('get_minimap_areas')
    return output


def is_camera_locked(img):
    ''' Returns is the camera is locked '''
    return (img[CAMERA_LOCK[::-1]] == [49, 65, 52]).all()
