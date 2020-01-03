'''Module that contains the analytics function'''
import time


class Analytics:
    '''Class to display and store analytics'''

    def __init__(self, logger):
        self.logger = logger
        self.timers = {}

    def start_timer(self, phase, message=None):
        '''Keeps track of start time of each phase and logs the message'''
        self.timers[phase] = time.time()
        if message is not None:
            self.logger.log(f'{message}...')

    def get_elapsed_time(self, phase):
        '''Calculates the elapsed time from phase start time'''
        if phase not in self.timers:
            return -1
        return time.time() - self.timers[phase]

    def end_timer(self, phase, message=None):
        '''Calculates and logs the time elapsed and stores it in a dict'''
        start_time = self.timers.pop(phase)
        time_elapsed = time.time() - start_time
        if message is not None:
            self.logger.log(f'{message}. Took {time_elapsed*1000}ms.')
        else:
            self.logger.log(f'Took {time_elapsed*1000}ms.')
