from tensorflow.keras.models import load_model
import numpy as np
import json


class prediction(object):
    def __init__(self):
        self.model = None
        self.classifier = None
        self.class_key_list = None

    def load_model(self, model_path):
        self.model = load_model(model_path)
        print(self.model.summary())

    def load_classifier(self, classifier_path):
        with open(classifier_path) as json_file:
            self.classifier = json.load(json_file)

        self.class_key_list = list(self.classifier.keys())

    def prediction(self, input_tensor, isLabeling=True):
        '''
        model prediction 이후, top1 값에 대한 labeling을 진행하여 return.
        '''
        #
        __pred = self.model.predict(input_tensor)
        if isLabeling == True:
            __label = self.labeling(__pred)
            return __label
        return __pred

    def labeling(self, result):
        __pred_res = result[0]
        __max_idx = np.argmax(__pred_res, axis=0)

        return self.class_key_list[__max_idx]

