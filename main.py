''' Main module of the script '''
import time

from analytics import Analytics
from logger import CliLogger
from screen import Screen
from resources import Resources
from window import find_rect
from lutils import wait_league_window
from ldetect import get_minimap_coor, get_minimap_areas


def main():
    '''Main function of the script'''
    logger = CliLogger()
    analytics = Analytics(logger)
    screen = Screen()
    resources = Resources()
    resources.load(analytics)

    hwnd = wait_league_window((0, 0, 1024, 768))

    while True:
        img = screen.screenshot(analytics, find_rect(hwnd))
        coor = get_minimap_coor(analytics, img)
        areas = get_minimap_areas(analytics, resources.images, coor)
        print(areas)
        time.sleep(1)


if __name__ == "__main__":
    main()
