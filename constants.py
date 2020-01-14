''' Stores the constants of the script '''

TICK_INTERVAL = 300, 600  # ms

LEVEL_UP_SEQUENCE = ['r', 'w', 'q', 'e']

COOLDOWNS = {'goto_lane': 3, 'goto_enemy_base': 3, 'evade': 0.2, 'move_forward': 0.5}

ANALYTICS_IGNORE = [
    'screenshot',
    'get_minimap_coor',
    'get_minimap_areas',
    'get_objects'
]
