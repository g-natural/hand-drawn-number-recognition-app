# Character Recognition Neural Network
import numpy as np
import math
import pdb
from enum import Enum
import traceback

class CRNNetwork:

    def __init__(self, input_ncount, hidden_ncount,
                 output_ncount, bias=0.5, learn_rate=0.005,
                 epoch=75):
        self.input_ncount = input_ncount
        self.hidden_ncount = hidden_ncount
        self.output_ncount = output_ncount
        self.bias = bias
        self.learn_rate = learn_rate
        self.epoch = epoch

        self.hidden_weights = np.random.uniform(low=-0.5, high=0.5,
                                size=(self.input_ncount, self.hidden_ncount))

        # extra vector to hold biases (i0 weights)
        self.hiddenl_bias = np.full([self.hidden_ncount], bias,
                                    dtype=float)
        self.output_weights = np.random.uniform(low=-0.5, high=0.5,
                                size=(self.hidden_ncount, self.output_ncount))
        # (h0 weights)
        self.outputl_bias = np.full([self.output_ncount], bias,
                                    dtype=float)

    def __actv_fun(self, x):
        # Sigmoid Function (1 / 1+e^(-x) )
        return 1 / (1 + math.exp(-x))

    def __layer_output(self, input_vector, layer_weights, layer_bias):

        layer_output = np.dot(input_vector, layer_weights)
        for i in range(len(layer_output)):
            layer_output[i] = self.__actv_fun(layer_output[i]
                                              + layer_bias[i])
        return layer_output

    def __outputl_error_vector(self, o_vector, t_vector):
        error_vector = np.empty([1,len(o_vector)])
        for i in range(len(o_vector)):
            error_vector[0,i] = (o_vector[i]*(1-o_vector[i])
                               * (t_vector[i]-o_vector[i]))


        return error_vector


    def __hiddenl_error_vector(self, hl_output, hl_targvec):
        error_vector = np.empty([1,len(hl_output)])
        for i in range(len(hl_output)):
            error_vector[0,i] = hl_output[i]*(1-hl_output[i])*hl_targvec[i]

        return error_vector

    def query_network(self, input_vector):
        hlayer_output = self.__layer_output(input_vector,
                                    self.hidden_weights, self.hiddenl_bias)
        output_vector = self.__layer_output(hlayer_output,
                                    self.output_weights, self.outputl_bias)
        return output_vector

    def train_network(self, input_matrix, input_labels, inst_count=None):
        #TODO: check for valid dimensions
        training_error_count = 0

        if inst_count:
            instance_count = inst_count
        else:
            instance_count = len(input_matrix)

        for run in range(self.epoch):
            
            for instance in range(instance_count):

                try:

                    hlayer_output = self.__layer_output(input_matrix[instance],
                                            self.hidden_weights, self.hiddenl_bias)
                    output_vector = self.__layer_output(hlayer_output,
                                            self.output_weights, self.outputl_bias)
                    target_vector = np.full([self.output_ncount, 1], 0.1, dtype=float)
                    target_vector[int(input_labels[instance])] = 0.99
               
                    ol_error_vector = self.__outputl_error_vector(output_vector,
                                                                 target_vector)
                    hlayer_target_vector = np.dot(self.output_weights, ol_error_vector.T)

                    hl_error_vector = self.__hiddenl_error_vector(hlayer_output,
                                                                  hlayer_target_vector)

                    d_output_weights = np.dot(hlayer_output.reshape([16,1]), ol_error_vector) * self.learn_rate
                    d_hidden_weights = np.dot(np.array([input_matrix[instance]]).T, hl_error_vector) * self.learn_rate
                    self.output_weights += d_output_weights
                    self.hidden_weights += d_hidden_weights
               
                    self.outputl_bias += (self.learn_rate * ol_error_vector[0])
                    self.hiddenl_bias += (self.learn_rate * hl_error_vector[0])

                except KeyboardInterrupt:
                    return
                except Exception as error:
                    error
                    training_error_count += 1
                    continue
