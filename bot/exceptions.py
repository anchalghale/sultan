''' Module for exceptions '''
from constants import TICK_INTERVAL


class BotExitException(Exception):
    ''' Raised when bot needs to be exited '''


class BotContinueException(Exception):
    ''' Raised when the current tick of the bot needs to be continued '''

    def __init__(self, tick_interval=TICK_INTERVAL):
        Exception.__init__(self)
        self.tick_interval = tick_interval
