'''
Module that handles tasks related to processes
'''
import os
import subprocess
import time

import psutil


def is_running(process_name):
    '''
    Check if there is any running process that contains
    the given name process_name.
    '''
    try:
        # Iterate over the all the running process
        for proc in psutil.process_iter():
            try:
                # Check if process name contains the given name string.
                if process_name.lower() in proc.name().lower():
                    return True
            except (psutil.NoSuchProcess,
                    psutil.AccessDenied, psutil.ZombieProcess):
                pass
    except TypeError:
        return False
    return False


def kill_process(process_name):
    '''
    Closes a process
    '''
    try:
        while True:
            try:
                for proc in psutil.process_iter():
                    if proc.name() == process_name:
                        proc.kill()
                if not is_running(process_name):
                    return
            except TypeError:
                pass
            time.sleep(1)
    except psutil.NoSuchProcess:
        return
