''' Object detection module '''
import cv2

from cutils import coor_offset, crop, find_center

from .constants import MINIMAP_AREAS, CAMERA_LOCK
from .exceptions import NoCharacterInMinimap


def detect(analytics, img, start, end):
    ''' Finds the league objects '''
    analytics.start_timer('in_range', 'Filtering using in range')
    size = img.shape[:2]
    img = cv2.inRange(img, start, end)
    contours, _ = cv2.findContours(img, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    objects = []
    for contour in contours:
        area = cv2.contourArea(contour)
        if area == 0:
            coor = tuple(contour[0][0])
            blue, green, red = img[coor_offset(coor, (27, 16), size)]
            if blue < 25 and green > 230 and red < 25:
                name = 'ally_champion'
            elif tuple(img[coor_offset(coor, (1, 1), size)]) == (208, 149, 77):
                name = 'ally_minion'
            else:
                name = 'enemy_minion'
            objects.append({
                'name': name,
                'coor': coor,
            })
    analytics.end_timer('in_range')
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
    analytics.end_timer('get_minimap_areas')
    return output


def is_camera_locked(img):
    ''' Returns is the camera is locked '''
    return (img[CAMERA_LOCK[::-1]] == [49, 65, 52]).all()
