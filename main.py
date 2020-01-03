''' Main module of the script '''
import time

import keyboard

from analytics import Analytics
from logger import CliLogger
from screen import Screen
from resources import Resources
from cooldown import Cooldown
from window import find_rect
from lutils import wait_league_window
from ldetect import is_camera_locked, is_level_up, get_minimap_coor, get_minimap_areas, get_objects
from bot import goto_lane, level_up
from constants import LEVEL_UP_SEQUENCE


def main():
    '''Main function of the script'''
    logger = CliLogger()
    analytics = Analytics(logger)
    analytics.ignore = ['screenshot', 'get_minimap_coor',
                        'get_minimap_areas', 'get_objects']
    screen = Screen()
    resources = Resources()
    cooldown = Cooldown({'goto_lane': 20})
    resources.load(analytics)

    hwnd = wait_league_window(logger, (0, 0, 1024, 768))
    time.sleep(1)

    logger.log('Press and hold x to exit bot.')
    while True:
        analytics.start_timer()
        if keyboard.is_pressed('x'):
            break
        img = screen.screenshot(analytics, find_rect(hwnd))
        if not is_camera_locked(img):
            keyboard.press_and_release('y')
        level_ups = is_level_up(img)
        level_up(level_ups, LEVEL_UP_SEQUENCE)
        coor = get_minimap_coor(analytics, img)
        areas = get_minimap_areas(analytics, resources.images, coor)
        if not areas['is_map_divide']:
            goto_lane(cooldown)
        print(get_objects(analytics, img, (227, 0, 228), (255, 1, 255)))
        analytics.end_timer()
        time.sleep(1)


if __name__ == "__main__":
    main()
