''' Main module of the script '''
import time
import traceback
import random

import keyboard

from analytics import Analytics
from logger import CliLogger
from screen import Screen
from resources import Resources
from cooldown import Cooldown
from window import find_rect, CantForgroundWindowError
from lvision import NoCharacterInMinimap
from llogic import Logic
from lutils import wait_league_window
from bot.exceptions import BotContinueException, BotExitException
from constants import ANALYTICS_IGNORE, COOLDOWNS, TICK_INTERVAL

from utils import Utility


def main():
    '''Main function of the script'''
    paused = False

    logger = CliLogger()
    screen = Screen()
    resources = Resources()
    analytics = Analytics(logger)
    cooldown = Cooldown(COOLDOWNS)
    analytics.ignore = ANALYTICS_IGNORE
    resources.load(analytics)
    utility = Utility(logger, screen, resources, analytics, cooldown)
    logic = Logic(utility)
    try:
        handle = wait_league_window(logger, (0, 0, 1024, 768))
    except CantForgroundWindowError:
        pass
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
            logic.tick()
            time.sleep(random.randint(*TICK_INTERVAL)/1000)
        except BotContinueException as exp:
            time.sleep(random.randint(*exp.tick_interval)/1000)
        except NoCharacterInMinimap:
            time.sleep(1)
        except BotExitException:
            screen.d3d.stop()
            break
        except Exception:  # pylint:disable=broad-except
            traceback.print_exc()
            screen.d3d.stop()
            break


if __name__ == "__main__":
    main()
