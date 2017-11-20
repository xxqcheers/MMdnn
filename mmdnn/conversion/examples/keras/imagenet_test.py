#----------------------------------------------------------------------------------------------
#  Copyright (c) Microsoft Corporation. All rights reserved.
#  Licensed under the MIT License. See License.txt in the project root for license information.
#----------------------------------------------------------------------------------------------

import argparse
import numpy as np
import sys
import os
from mmdnn.conversion.examples.imagenet_test import TestKit


class TestKeras(TestKit):

    def __init__(self):
        super(TestKeras, self).__init__()
        self.model = self.MainModel.KitModel(self.args.w)


    def preprocess(self, image_path):
        x = super(TestKeras, self).preprocess(image_path)
        self.data = np.expand_dims(x, 0)


    def print_result(self):
        predict = self.model.predict(self.data)
        super(TestKeras, self).print_result(predict)


    def print_intermediate_result(self, layer_name, if_transpose = False):
        from keras.models import Model
        intermediate_layer_model = Model(inputs = self.model.input,
                                         outputs = self.model.get_layer(layer_name).output)
        intermediate_output = intermediate_layer_model.predict(self.data)
        super(TestKeras, self).print_intermediate_result(intermediate_output, if_transpose)

    
    def inference(self, image_path):
        self.preprocess(image_path)

        #self.print_intermediate_result('pool1_norm1', True)

        self.print_result()

        self.test_truth()


    def dump(self, path = None):
        if path is None: path = self.args.dump
        self.model.save(path)
        print ('Keras model file is saved as [{}], generated by [{}.py] and [{}].'.format(
            path, self.args.n, self.args.w))


if __name__=='__main__':
    tester = TestKeras()
    if tester.args.dump:
        tester.dump()
    else:
        tester.inference(tester.args.image)
