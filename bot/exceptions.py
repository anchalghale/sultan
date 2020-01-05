''' Module for exceptions '''


class BotExitException(Exception):
    ''' Raised when bot needs to be exited '''


class BotContinueException(Exception):
    ''' Raised when the current tick of the bot needs to be continued '''
