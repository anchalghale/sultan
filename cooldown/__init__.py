'''Module that contains the cooldown function'''
import time


class Cooldown:
    '''Class to display and store cooldown'''

    def __init__(self, cooldowns):
        self.timers = {}
        self.cooldowns = cooldowns

    def start_timer(self, task=''):
        '''Keeps track of start time of each task'''
        self.timers[task] = time.time()

    def get_elapsed_time(self, task=''):
        '''Calculates the elapsed time from task start time'''
        if task not in self.timers:
            return -1
        return time.time() - self.timers[task]

    def is_available(self, task=''):
        '''Calculates the elapsed time from task start time'''
        if task not in self.timers:
            return True
        if task not in self.cooldowns:
            return True
        if self.get_elapsed_time(task) >= self.cooldowns[task]:
            return True
        return False

    def end_timer(self, task=''):
        '''Calculates and logs the time elapsed and stores it in a dict'''
        return self.timers.pop(task)
