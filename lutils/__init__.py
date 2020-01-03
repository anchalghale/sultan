''' League of legends utility functions '''
import time
from process import is_running


def check_and_wait():
    ''' Waits for the game to start '''
    if not is_running('League of Legends.exe'):
        print('Wating for the game to start...')
        while True:
            if is_running('League of Legends.exe'):
                return True
            time.sleep(10)
    return False
