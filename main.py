''' Main module of the script '''

import time
import collections

import keyboard
import mouse

from analytics import Analytics
from logger import CliLogger
from screen import Screen
from resources import Resources
from cooldown import Cooldown
from window import find_rect

from lutils import wait_league_window
from lvision.filter import filter_objects
from lvision.state import get_game_state
from lvision import (is_camera_locked, get_level_ups,
                     get_minimap_coor, get_minimap_areas, get_objects)


from bot.exceptions import BotContinueException, BotExitException
from bot import goto_lane, goto_enemy_base, evade, level_up

from constants import LEVEL_UP_SEQUENCE, ANALYTICS_IGNORE, COOLDOWNS

Utility = collections.namedtuple('Utility', 'logger screen resources analytics cooldown')


def tick(utility, handle):
    ''' Simulates a single tick of the bot '''
    utility.analytics.start_timer()
    if keyboard.is_pressed('x'):
        raise BotExitException
    img = utility.screen.screenshot(utility.analytics, find_rect(handle))
    if not is_camera_locked(img):
        keyboard.press_and_release('y')
    level_ups = get_level_ups(img)
    level_up(level_ups, LEVEL_UP_SEQUENCE)
    coor = get_minimap_coor(utility.analytics, img)
    areas = get_minimap_areas(utility.analytics, utility.resources.images, coor)
    obj_list = get_objects(utility.analytics, img, (190, 0, 190), (255, 20, 255))
    objects = filter_objects(obj_list)
    state = get_game_state(obj_list, areas)

    if state.is_enemy_turret and not state.is_shielded:
        evade(utility.cooldown)
        raise BotContinueException
    if state.is_enemy_turret and state.is_shielded:
        mouse.move(*objects.turrets[0]['coor'])
        mouse.click()
        raise BotContinueException
    if objects.enemy_minions != []:
        objects.enemy_minions.sort(key=lambda o: o['health'])
        mouse.move(*objects.enemy_minions[0]['center'])
        mouse.click()
        raise BotContinueException
    if areas['is_turret']:
        if len(objects.shield_minions) <= 2:
            goto_lane(utility.cooldown)
            raise BotContinueException
    if not (areas['is_chaos_side'] and areas['is_lane']):
        goto_lane(utility.cooldown)
        raise BotContinueException
    if len(objects.shield_minions) > 2:
        goto_enemy_base(utility.cooldown)


def main():
    '''Main function of the script'''

    logger = CliLogger()
    screen = Screen()
    resources = Resources()
    analytics = Analytics(logger)
    cooldown = Cooldown(COOLDOWNS)
    analytics.ignore = ANALYTICS_IGNORE
    resources.load(analytics)
    hwnd = wait_league_window(logger, (0, 0, 1024, 768))
    logger.log('Press and hold x to exit bot.')
    while True:
        try:
            tick(Utility(logger, screen, resources, analytics, cooldown), hwnd)
            analytics.end_timer()
            time.sleep(1)
        except BotContinueException:
            analytics.end_timer()
            time.sleep(1)
        except BotExitException:
            break


if __name__ == "__main__":
    main()
