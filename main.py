''' Main module of the script '''
import time
import collections
import traceback
import random

import keyboard

from analytics import Analytics
from logger import CliLogger
from screen import Screen
from resources import Resources
from cooldown import Cooldown
from window import find_rect
from llogic import Logic
from lutils import wait_league_window
from bot.exceptions import BotContinueException, BotExitException
from constants import ANALYTICS_IGNORE, COOLDOWNS

Utility = collections.namedtuple('Utility', 'logger screen resources analytics cooldown')

TICK_INTERVAL = 300, 600  # ms


def main():
    '''Main function of the script'''
    paused = False

    logic = Logic()
    logger = CliLogger()
    screen = Screen()
    resources = Resources()
    analytics = Analytics(logger)
    cooldown = Cooldown(COOLDOWNS)
    analytics.ignore = ANALYTICS_IGNORE
    resources.load(analytics)
    utility = Utility(logger, screen, resources, analytics, cooldown)
    handle = wait_league_window(logger, (0, 0, 1024, 768))
    logger.log('Press and hold x to exit bot.')
    screen.d3d.capture(target_fps=10, region=find_rect(handle))
    while True:
        try:
            if keyboard.is_pressed('x'):
                raise BotExitException
            if keyboard.is_pressed('ctrl+u'):
                paused = False
            if paused:
                time.sleep(0.1)
                continue
            if keyboard.is_pressed('ctrl+p'):
                paused = True
                logger.log('Bot paused. Press ctrl+u to unpause. Press x to exit.')
                continue
            logic.tick(utility)
            time.sleep(random.randint(*TICK_INTERVAL)/1000)
        except BotContinueException:
            time.sleep(random.randint(*TICK_INTERVAL)/1000)
        except BotExitException:
            screen.d3d.stop()
            break
        except Exception:  # pylint:disable=broad-except
            traceback.print_exc()
            screen.d3d.stop()
            break


if __name__ == "__main__":
    main()
