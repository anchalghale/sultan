
''' Moudle for window management using only ctypes '''
import ctypes
from ctypes import wintypes
from collections import namedtuple

USER32 = ctypes.WinDLL('user32', use_last_error=True)

WindowInfo = namedtuple('WindowInfo', 'pid title')

WNDENUMPROC = ctypes.WINFUNCTYPE(
    wintypes.BOOL,
    wintypes.HWND,    # _In_ hWnd
    wintypes.LPARAM,)  # _In_ lParam


def get_windows():
    '''Return a sorted list of visible windows.'''
    result = []
    @WNDENUMPROC
    def enum_proc_cb(hwnd, l_param):
        ''' Callback for enum windows '''
        try:
            if USER32.IsWindowVisible(hwnd):
                pid = wintypes.DWORD()
                _ = USER32.GetWindowThreadProcessId(
                    hwnd, ctypes.byref(pid))
                length = USER32.GetWindowTextLengthW(hwnd) + 1
                title = ctypes.create_unicode_buffer(length)
                USER32.GetWindowTextW(hwnd, title, length)
                result.append(WindowInfo(pid.value, title.value))
        except ctypes.ArgumentError:
            pass
        return True
    USER32.EnumWindows(enum_proc_cb, 0)
    return sorted(result)
