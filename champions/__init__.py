''' Module that contains champion logic '''

from ._ashe import CHAMPION as ashe
from ._caitlyn import CHAMPION as caitlyn
from ._miss_fortune import CHAMPION as miss_fortune
from ._tristana import CHAMPION as tristana
from ._sivir import CHAMPION as sivir


CHAMPIONS_MAPPING = {
    'caitlyn': caitlyn,
    'ashe': ashe,
    'sivir': sivir,
    'tristana': tristana,
    'miss_fortune': miss_fortune,
}


def get_champion_class(name):
    '''Returns a champion class from name'''
    if name not in CHAMPIONS_MAPPING:
        return caitlyn
    return CHAMPIONS_MAPPING[name]
