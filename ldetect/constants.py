''' Stores the constants of the script '''
CAMERA_LOCK = (794, 756)

MINIMAP_AREAS = [
    {
        'name': 'is_base',
        'file_name': 'getisbase',
        'mappings': {
            (0, 0, 0): False,
            (0, 255, 0): True,
        }
    },
    {
        'name': 'is_lane',
        'file_name': 'getislane',
        'mappings': {
            (0, 0, 0): False,
            (0, 255, 0): True,
        }
    },
    {
        'name': 'is_map_divide',
        'file_name': 'getisneutralmapdivide',
        'mappings': {
            (0, 0, 0): False,
            (0, 255, 0): True,
        }
    },
    {
        'name': 'is_order_side',
        'file_name': 'getisorderside',
        'mappings': {
            (0, 0, 0): False,
            (0, 255, 0): True,
        }
    },
    {
        'name': 'is_platform',
        'file_name': 'getisplatform',
        'mappings': {
            (0, 0, 0): False,
            (0, 255, 0): True,
        }
    },
    {
        'name': 'is_turret',
        'file_name': 'getisturret',
        'mappings': {
            (0, 0, 0): False,
            (0, 255, 0): True,
        }
    },
    {
        'name': 'nearest_lane',
        'file_name': 'getnearestlane',
        'mappings': {
            (255, 0, 0): 'top',
            (0, 255, 0): 'mid',
            (0, 0, 255): 'bot',
        }
    },
]
