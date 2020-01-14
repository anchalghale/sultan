''' Utility functions '''

import collections

Champion = collections.namedtuple(
    'Champion',
    'orb_walk_champion poke_champion kite_champion attack_turret attack_minion '
    'kite_minion orb_walk_minion attack_structure ')
