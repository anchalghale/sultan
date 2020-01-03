''' League of legends utility functions '''
import time
from process import is_running

from window import find_window_hwnds, move_window_hwnd, focus_window, NoWindowFoundError


def check_and_wait():
    ''' Waits for the game to start '''
    if not is_running('League of Legends.exe'):
        print('Wating for the game to start...')
        while True:
            if is_running('League of Legends.exe'):
                return True
            time.sleep(10)
    return False


def wait_league_window(rect):
    ''' Waits league of legends window '''
    print('Wating for the league of legends window...')
    while True:
        try:
            hwnd = find_window_hwnds(r'League of Legends \(TM\) Client')[0]
            move_window_hwnd(hwnd, rect)
            focus_window(hwnd)
            return hwnd
        except NoWindowFoundError:
            time.sleep(10)
