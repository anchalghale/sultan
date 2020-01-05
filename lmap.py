''' Main module of the get objects function test '''
import time

import keyboard
import cv2

from analytics import Analytics
from logger import CliLogger
from screen import Screen
from window import find_rect
from lutils import wait_league_window
from ldetect import get_minimap_coor

TURRET_LOCATIONS = [(54, 9)]


def get_turret_coors(analytics, img):
    analytics.start_timer()
    coor = get_minimap_coor(analytics, img)
    width = 36
    height = 27
    pt1 = (coor[1]-width//2-1, coor[0]-height//2-1)
    pt2 = (coor[1]+width//2-2, coor[0]+height//2-1)
    turret_coor = []
    for turret in TURRET_LOCATIONS:
        if pt1[0] < turret[0] < pt2[0] and pt1[1] < turret[1] < pt2[1]:
            offset = [turret[0]-pt1[0], turret[1]-pt1[1]]
            scale = img.shape[1]/width
            offset = tuple([int(v * scale) for v in offset])
            turret_coor.append(offset)
            # print('offset', offset)
    analytics.end_timer()

    img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
    overlay = img.copy()
    output = img.copy()
    for coor in turret_coor:
        img = cv2.circle(overlay, coor, 300, (0, 0, 255, 30), -1)
    alpha = 0.4
    cv2.addWeighted(overlay, alpha, output, 1 - alpha, 0, output)
    cv2.imshow('', output)
    cv2.waitKey(1)

    # map_ = crop(img, (834, 577, 183, 183))
    # map_ = cv2.rectangle(map_, pt1, pt2, (0, 255, 0), 1)
    # map_ = cv2.resize(map_, (0, 0), fx=3, fy=3, interpolation=cv2.INTER_NEAREST)
    # cv2.imshow('Map', map_)


def main():
    '''Main function of the script'''
    logger = CliLogger()
    analytics = Analytics(logger)
    analytics.ignore = ['screenshot', 'get_minimap_coor',
                        'get_minimap_areas', 'get_objects']
    screen = Screen()
    hwnd = wait_league_window(logger, (0, 0, 1024, 768))
    time.sleep(1)

    logger.log('Press and hold x to exit bot.')
    while True:
        analytics.start_timer()
        if keyboard.is_pressed('x'):
            break
        img = screen.screenshot(analytics, find_rect(hwnd))
        get_turret_coors(analytics, img)
        time.sleep(1)


if __name__ == "__main__":
    main()
