''' Stores the constants of the script '''
CAMERA_LOCK = (794, 756)
LEVEL_Q = (416, 687)
LEVEL_W = (448, 687)
LEVEL_E = (479, 687)
LEVEL_R = (510, 687)
POINT_Q = (406, 738)
POINT_W = (438, 738)
POINT_E = (469, 738)
POINT_R = (505, 738)
Q = (404, 706)
W = (435, 706)
E = (467, 706)
R = (498, 706)

MINIMAP_AREAS = [
    {
        'file_name': 'getisbase',
        'mappings': {
            (0, 0, 0): False,
            (0, 255, 0): True,
        }
    },
    {
        'file_name': 'getislane',
        'mappings': {
            (0, 0, 0): False,
            (0, 255, 0): True,
        }
    },
    {
        'file_name': 'getisneutralmapdivide',
        'mappings': {
            (0, 0, 0): False,
            (0, 255, 0): True,
        }
    },
    {
        'file_name': 'getisorderside',
        'mappings': {
            (0, 0, 0): False,
            (0, 255, 0): True,
        }
    },
    {
        'file_name': 'getisplatform',
        'mappings': {
            (0, 0, 0): False,
            (0, 255, 0): True,
        }
    },
    {
        'file_name': 'getisturret',
        'mappings': {
            (0, 0, 0): False,
            (0, 255, 0): True,
        }
    },
    {
        'file_name': 'getnearestlane',
        'mappings': {
            (255, 0, 0): 'top',
            (0, 255, 0): 'mid',
            (0, 0, 255): 'bot',
        }
    },
]
