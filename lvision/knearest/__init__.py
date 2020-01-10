'''Module that performs ocr'''
import cv2
import numpy as np


class KNearest:
    '''Class for object recognition'''

    def __init__(self, threshold=None, model_path=None):
        self.model = None
        self.threshold = threshold
        if model_path is not None:
            self.load_model(model_path)

    def load_model(self, path):
        '''Load model from given path'''
        self.model = cv2.ml.KNearest_load(path)

    def predict(self, image):
        '''Predict number in image'''
        img = image.reshape((1, image.shape[0]*image.shape[1]))
        data = np.float32(img)
        _, results, _, dists = self.model.findNearest(data, k=1)
        return int((results[0][0])) if self.threshold is None or int(dists[0][0]) < self.threshold else ''

    def train(self, samples, responses):
        '''Train the model'''
        self.model = cv2.ml.KNearest_create()
        self.model.train(samples, cv2.ml.ROW_SAMP2LE, responses)

    def save_model(self, path):
        '''Save model to given path'''
        self.model.save(path)
