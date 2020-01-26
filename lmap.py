''' Main module of the get objects function test '''
import time

import keyboard
import cv2

from analytics import Analytics
from logger import CliLogger
from screen import Screen
from window import find_rect
from lutils import wait_league_window
from lvision import get_minimap_coor


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
        if keyboard.is_pressed('x'):
            break
        img = screen.screenshot(find_rect(hwnd))
        time.sleep(1)


if __name__ == "__main__":
    main()
