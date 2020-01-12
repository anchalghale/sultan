'''Module that contains the analytics function'''
import time

from logger import CliLogger


class Analytics:
    '''Class to display and store analytics'''

    def __init__(self, logger=None):
        self.logger = CliLogger() if logger is None else logger
        self.timers = {}
        self.ignore = []

    def start_timer(self, phase='', message=None):
        '''Keeps track of start time of each phase and logs the message'''
        if phase in self.ignore:
            return
        self.timers[phase] = time.time()
        if message is not None:
            self.logger.log(f'{message}...')

    def get_elapsed_time(self, phase=''):
        '''Calculates the elapsed time from phase start time'''
        if phase not in self.timers:
            return -1
        return time.time() - self.timers[phase]

    def end_timer(self, phase='', message=None):
        '''Calculates and logs the time elapsed and stores it in a dict'''
        if phase in self.ignore:
            return
        start_time = self.timers.pop(phase)
        time_elapsed = time.time() - start_time
        if message is not None:
            self.logger.log(f'{message}. Took {time_elapsed*1000}ms.')
        else:
            self.logger.log(f'Took {time_elapsed*1000}ms.')
