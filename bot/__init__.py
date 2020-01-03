''' Tasks that bot performs using keyboard and mouse '''
import mouse
import keyboard

from cutils import humanize


def goto_lane(cooldown):
    ''' Goto a lane '''
    # Currently moves to top lane only
    if not cooldown.is_available('goto_lane'):
        return
    print('moving to lane')
    mouse.move(*humanize((862, 607)))
    mouse.right_click()
    cooldown.start_timer('goto_lane')


def level_up(level_ups, sequence):
    ''' Levels up an ability using priority sequence '''
    for ability in sequence:
        if level_ups[ability]:
            print(f'leveling up {ability}')
            keyboard.press_and_release(f'ctrl+{ability}')
            return
