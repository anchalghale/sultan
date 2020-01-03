'''Moudle for window management'''
import re
import os

import win32con
import win32gui


class NoWindowFoundError(Exception):
    ''' Raised when no window exists '''


class CantForgroundWindowError(Exception):
    ''' Raised when window couldn't be foregrounded '''


def window_enum_callback(hwnd, args):
    ''' Pass to win32gui.EnumWindows() to check all the opened windows '''
    if re.fullmatch(args[0], str(win32gui.GetWindowText(hwnd))) is not None:
        args[1].append(hwnd)


def find_window_hwnds(wildcard):
    ''' Find a window whose title matches the wildcard regex '''
    result = []
    args = [wildcard, result]
    win32gui.EnumWindows(window_enum_callback, args)
    if result == []:
        raise NoWindowFoundError
    return args[1]


def find_rect(hwnd):
    ''' Returns the bounding rectangle of window '''
    return win32gui.GetWindowRect(hwnd)


def move_window_hwnd(hwnd, rect):
    ''' Moves the window to a rectangle using hwnd '''
    try:
        win32gui.MoveWindow(hwnd, rect[0], rect[1], rect[2], rect[3], True)
        return True
    except win32gui.error:
        return False


def focus_window(hwnd):
    ''' Returns the bounding rectangle of window '''
    try:
        win32gui.ShowWindow(hwnd, win32con.SW_RESTORE)
        win32gui.SetWindowPos(hwnd, win32con.HWND_NOTOPMOST, 0, 0,
                              0, 0, win32con.SWP_NOMOVE + win32con.SWP_NOSIZE)
        win32gui.SetWindowPos(hwnd, win32con.HWND_TOPMOST, 0, 0,
                              0, 0, win32con.SWP_NOMOVE + win32con.SWP_NOSIZE)
        win32gui.SetWindowPos(
            hwnd, win32con.HWND_NOTOPMOST, 0, 0, 0, 0,
            (
                win32con.SWP_SHOWWINDOW +
                win32con.SWP_NOMOVE +
                win32con.SWP_NOSIZE
            ))
        win32gui.SetForegroundWindow(hwnd)
    except win32gui.error:
        raise CantForgroundWindowError


def close_window(handle):
    ''' Finds and closes a window with a handle '''
    try:
        if handle is not None:
            win32gui.PostMessage(handle, win32con.WM_CLOSE, 0, 0)
    except win32gui.error:
        pass
