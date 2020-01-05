''' Main script of tile designer '''
import tkinter as tk
import threading
import time
from tkinter import filedialog

import cv2
import pygubu
import numpy
import keyboard

from analytics import Analytics
from logger import CliLogger

from builder import Builder
from window import find_window_hwnds, find_rect, NoWindowFoundError
from screen import Screen
from lvision import get_minimap_coor
from lvision.exceptions import NoCharacterInMinimap


class Application:
    ''' The tkinter application class '''

    def __init__(self, root):
        builder = pygubu.Builder()
        builder.add_from_file('ldesigner/gui.ui')
        builder.get_object('main_frame', root)
        builder.connect_callbacks(self)
        root.title('League of Legends Tile Designer')
        root.geometry('640x480+0+480')
        logger = CliLogger('%H:%M:%S')
        keyboard.add_hotkey('a', self.set_true)
        keyboard.add_hotkey('s', self.set_false)
        self.analytics = Analytics(logger)
        self.builder = Builder(builder)
        self.screen = Screen()
        self.tiles = numpy.zeros((183, 183, 3), numpy.uint8)
        self.coor = None
        threading.Thread(target=self.monitor_league, daemon=True).start()

    def monitor_league(self):
        ''' Monitors league for detecting coordinate of character in minimap '''
        while True:
            try:
                hwnds = find_window_hwnds(r'League of Legends \(TM\) Client')
                rect = find_rect(hwnds[0])
                img = self.screen.screenshot(self.analytics, rect)
                self.coor = get_minimap_coor(self.analytics, img)
                self.builder.set_entry('coor', self.coor)
                self.builder.set_entry('value', self.tiles[self.coor])
                tiles_copy = self.tiles.copy()
                cv2.circle(tiles_copy, self.coor[::-1], 3, (255, 0, 0))
                tiles_copy = cv2.resize(
                    tiles_copy, (0, 0), fx=2, fy=2, interpolation=cv2.INTER_NEAREST)
                cv2.imshow('', tiles_copy)
                cv2.waitKey(1)
                cv2.moveWindow('', 0, 0)
                time.sleep(0.5)
            except NoWindowFoundError:
                time.sleep(5)
            except NoCharacterInMinimap:
                time.sleep(5)

    def import_(self):
        ''' Import the tile data '''
        file = filedialog.askopenfilename()
        if file is not None:
            self.tiles = cv2.imread(file)

    def export(self):
        ''' Export the tile data '''
        file = filedialog.asksaveasfilename()
        if file is not None:
            if file[-4:] != '.png':
                file += '.png'
            cv2.imwrite(file, self.tiles)

    def set_true(self):
        ''' Sets a tile to true '''
        self.tiles[self.coor] = [0, 255, 0]

    def set_false(self):
        ''' Sets a tile to false '''
        self.tiles[self.coor] = [0, 0, 0]


def main():
    ''' Main function of the script '''
    root = tk.Tk()
    Application(root)
    root.mainloop()


if __name__ == "__main__":
    main()
