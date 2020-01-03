''' Main module of the script '''
import uuid

import d3dshot
import cv2

from analytics import Analytics
from logger import CliLogger
from screen import Screen
from window import find_rect
from lutils import wait_league_window
from cutils import crop


def main():
    '''Main function of the script'''
    logger = CliLogger()
    analytics = Analytics(logger)
    screen = Screen()
    hwnd = wait_league_window((0, 0, 1024, 768))

    def name():
        return f'helper/output/{uuid.uuid1()}.png'

    img = screen.screenshot(analytics, find_rect(hwnd))
    cv2.imwrite(name(), crop(img, (629, 752, 7, 9)))
    cv2.imwrite(name(), crop(img, (636, 752, 7, 9)))
    cv2.imwrite(name(), crop(img, (643, 752, 7, 9)))
    cv2.imwrite(name(), crop(img, (650, 752, 7, 9)))
    cv2.imwrite(name(), crop(img, (657, 752, 7, 9)))
    cv2.imwrite(name(), crop(img, (664, 752, 7, 9)))


if __name__ == "__main__":
    main()
