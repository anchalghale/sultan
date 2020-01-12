''' Main module of the script '''
import uuid
import os
import glob
import argparse
import tkinter
from tkinter.simpledialog import askstring

from PIL import Image, ImageTk
import cv2

from analytics import Analytics
from logger import CliLogger
from screen import Screen
from window import find_rect
from lutils import wait_league_window
from cutils import crop


def lfilter(function, iterable):
    ''' Filters a list and outputs a list value '''
    return list(filter(function, iterable))


def name(label):
    ''' Creates a name for the output image '''
    directory = f'helper/output/{label}'
    os.makedirs(directory, exist_ok=True)
    return f'{directory}/{uuid.uuid1()}.png'


def export_data(label_input, change_img, img, rect):
    ''' Asks for label value and writes to file '''
    img = crop(img, rect)
    img_rgb = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
    tk_img = ImageTk.PhotoImage(image=Image.fromarray(img_rgb))
    change_img(tk_img)
    label = label_input()
    if label == 'exit':
        raise Exception
    if label in ['', None]:
        return
    cv2.imwrite(name(label), img)


def tick(label_input, change_img, img):
    ''' Simulates a single tick of the bot '''
    # export_data(label_input, change_img, img, (534, 707, 19, 16))  # sums 1
    # export_data(label_input, change_img, img, (558, 707, 19, 16))  # sums 2
    export_data(label_input, change_img, img, (596, 709, 12, 12))  # item 1
    export_data(label_input, change_img, img, (619, 709, 12, 12))  # item 1
    export_data(label_input, change_img, img, (642, 709, 12, 12))  # item 1
    export_data(label_input, change_img, img, (596, 731, 12, 12))  # item 1
    export_data(label_input, change_img, img, (619, 731, 12, 12))  # item 1
    export_data(label_input, change_img, img, (642, 731, 12, 12))  # item 1

    # export_data(label_input, change_img, img, (664, 709, 12, 12))  # trinklet 1


def main():
    '''Main function of the script'''
    root = tkinter.Tk()
    root.title('Training Data Generator')
    canvas = tkinter.Canvas(root, width=300, height=300)
    canvas.pack()
    canvas_img = canvas.create_image(20, 20, anchor="nw")
    root.mainloop(n=1)

    parser = argparse.ArgumentParser()
    parser.add_argument('--all', '-a', action='store_true')
    parser.add_argument('--interactive', '-i', action='store_true')

    args = parser.parse_args()

    logger = CliLogger()
    screen = Screen()
    analytics = Analytics(logger)

    def tick_gui(img):
        tick(lambda: askstring('Enter label. Type exit to stop.', root, parent=root),
             lambda i: canvas.itemconfig(canvas_img, image=i), img)

    if args.interactive:
        hwnd = wait_league_window(logger, (0, 0, 1024, 768))
        img = screen.screenshot(analytics, find_rect(hwnd))
        img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
        tick_gui(img)
        return
    if args.all:
        files = glob.glob('screenshots/*.png')
    else:
        files = [glob.glob('screenshots/*.png')[0]]
    for file in files:
        img = cv2.imread(file)
        tick_gui(img)


if __name__ == "__main__":
    main()
