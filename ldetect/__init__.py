''' Object detection module '''
import cv2

from cutils import coor_offset, crop, find_center, get_color_diff

from .constants import MINIMAP_AREAS, CAMERA_LOCK, LEVEL_Q, LEVEL_W, LEVEL_E, LEVEL_R
from .colors import SMALL_HP_BARS
from .exceptions import NoCharacterInMinimap


def get_small_hp_value(hp_img):
    ''' Calcuates the hp of given image of width 60 '''
    try:
        hp_img = hp_img.reshape((60, 3))
    except ValueError:
        return 60
    reference = hp_img[1]
    for i, value in enumerate(hp_img):
        if get_color_diff(reference, value) > 20:
            return i
    return 60


def identify_object(img, coor):
    ''' Indentify an object from the coordiate '''
    size = img.shape[:2]
    output = {'coor': coor}
    if (img[coor_offset(coor, (1, 0), size)] == (24, 239, 24)).all():
        output['name'] = 'ally_champion'
    elif tuple(img[coor_offset(coor, (0, -1), size)]) != (21, 1, 255):
        return None
    else:

        color = tuple(img[coor_offset(coor, (1, 0), size)])
        diffs = {}
        for key, value in SMALL_HP_BARS.items():
            diffs[key] = get_color_diff(value, color)
        output['name'] = sorted(diffs, key=diffs.get)[0]
        hp_bar = img[coor[1]:coor[1]+1, coor[0]+1:coor[0]+61]
        output['health'] = get_small_hp_value(hp_bar)
        output['center'] = coor[0]+30, coor[1]+35
        output['is_order_side'] = output['center'][1] / \
            output['center'][0] > img.shape[0]/img.shape[1]
    return output


def get_objects(analytics, img, start, end):
    ''' Finds the league objects '''
    analytics.start_timer('get_objects', 'Finding objects')
    threshed = cv2.inRange(img, start, end)
    contours, _ = cv2.findContours(
        threshed, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    objects = []
    for contour in contours:
        area = cv2.contourArea(contour)
        if area > 2000:
            objects.append({'name': 'turret', 'coor': tuple(contour[0][0])})
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
    img = cv2.inRange(map_, (200, 200, 200), (255, 255, 255))
    contours, _ = cv2.findContours(img, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    if contours == []:
        raise NoCharacterInMinimap
    box = sorted(contours, key=cv2.contourArea, reverse=True)[0]
    coor = find_center(cv2.boundingRect(box))
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


def is_level_up(img):
    ''' Returns is the camera is locked '''
    return {
        'Q': (img[LEVEL_Q[::-1]] == [255, 251, 173]).all(),
        'W': (img[LEVEL_W[::-1]] == [255, 251, 173]).all(),
        'E': (img[LEVEL_E[::-1]] == [255, 251, 173]).all(),
        'R': (img[LEVEL_R[::-1]] == [255, 251, 173]).all(),
    }
