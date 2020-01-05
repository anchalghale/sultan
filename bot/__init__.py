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
    mouse.move(*humanize((931, 663)))
    mouse.right_click()
    cooldown.start_timer('goto_lane')


def evade(cooldown):
    ''' Goto a lane '''
    if not cooldown.is_available('evade'):
        return
    print('evading')
    mouse.move(*humanize((27, 730)))
    mouse.right_click()
    cooldown.start_timer('evade')


def goto_enemy_base(cooldown):
    ''' Goto enemy base '''
    if not cooldown.is_available('goto_enemy_base'):
        return
    print('moving to enemy base')
    mouse.move(*humanize((988, 605)))
    mouse.right_click()
    cooldown.start_timer('goto_enemy_base')


def level_up(level_ups, ability_points, sequence):
    ''' Levels up an ability using priority sequence '''
    for ability in sequence:
        if getattr(level_ups, ability) and not getattr(ability_points, ability):
            print(f'leveling up {ability}')
            keyboard.press_and_release(f'ctrl+{ability}')
            return

    for ability in sequence:
        if getattr(level_ups, ability):
            print(f'leveling up {ability}')
            keyboard.press_and_release(f'ctrl+{ability}')
            return
