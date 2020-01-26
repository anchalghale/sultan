''' Main module of the get objects function test '''
import uuid
import os

import cv2
import keyboard

from logger import Logger, CliLogger
from screen import Screen


from lutils import wait_league_window
from window import find_rect


def name():
    ''' Creates a name for the output image '''
    directory = 'helper/screenshots'
    os.makedirs(directory, exist_ok=True)
    return f'{directory}/{uuid.uuid1()}.png'


def export_data(logger: Logger, img):
    ''' Asks for label value and writes to file '''
    file_name = name()
    img_bgr = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
    logger.log(f'Saving to {file_name}')
    cv2.imwrite(file_name, img_bgr)


def main():
    '''Main function of the script'''
    logger = CliLogger()
    screen = Screen()

    handle = wait_league_window(logger, (0, 0, 1024, 768))
    rect = find_rect(handle)

    logger.log('Window found.')
    logger.log('ctrl+s to save')
    logger.log('ctrl+w to exit')

    def screenshot():
        nonlocal logger, screen, rect
        img = screen.screenshot(rect)
        export_data(logger, img)

    keyboard.add_hotkey('ctrl+s', screenshot)
    keyboard.wait('ctrl+w')


if __name__ == "__main__":
    main()
