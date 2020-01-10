''' Manages the assets of the bot '''
import os
import glob

import cv2

from lvision.knearest import KNearest


class Resources:
    ''' Manages the assets of the bot '''

    def __init__(self):
        self.images = {}
        self.models = {}

    def load(self, analytics):
        ''' Loads the resources file into memory '''
        analytics.start_timer('load_resources', 'Loading resources')
        for file in glob.glob('lvision/assets/images/**/*.png'):
            base_name = os.path.basename(file)
            name = os.path.splitext(base_name)[0]
            self.images[name] = cv2.imread(file)
        for file in glob.glob('lvision/knearest/trained/*.yml'):
            base_name = os.path.basename(file)
            name = os.path.splitext(base_name)[0]
            threshold = None
            if name == 'gold':
                threshold = 200000
            knearest = KNearest(threshold=threshold)
            knearest.load_model(file)

            self.models[name] = knearest
        analytics.end_timer('load_resources', 'Loading resources')
