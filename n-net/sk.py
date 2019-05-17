import numpy as np
import scipy.special as sci

class neuralNetwork:

    def __init__(self,inputnodes,hiddennodes,outputnodes,learningrate):
        self.inodes=inputnodes
        self.hnodes=hiddennodes
        self.onodes=outputnodes

        #матрицы весовых коэфицентов
        self.wih = np.random.normal(0.0, pow(self.hnodes, -0.5),(self.hnodes, self.inodes))
        self.who = np.random.normal(0.0, pow(self.onodes, -0.5),(self.onodes, self.hnodes))

        self.lr=learningrate

        #функция актифации - сигмойда
        self.activation_func= lambda x: sci.expit(x)

    def train():
        # ыходные значения в двумерный масив
        inputs = np.array(inputs_list, ndmin=2).T
        targets = np.array(targets_list, ndmin=2).T

        # расчёт входящих сигналов для скрытово слоя
        hidden_inputs = np.dot(self.wih, inputs)
        # сигнал  исходящие для скрытого слоя
        hidden_outputs = self.activation_function(hidden_inputs)

        # входящие для выходного слоя
        final_inputs = np.dot(self.who, hidden_outputs)
        # исходящие для выходного слоя
        final_outputs = self.activation_function(final_inputs)

        # ошибки выходного слоя (целевое знач. - фактическое знач.)
        output_errors = targets - final_outputs
        # hidden layer error is the output_errors, split by weights, recombined at hidden nodes
        hidden_errors = np.dot(self.who.T, output_errors)

        # обновление весов связей слоёв скрытый--выходной
        self.who += self.lr * np.dot((output_errors * final_outputs * (1.0 - final_outputs)), np.transpose(hidden_outputs))

        # обновление весов связей слоёв выходной--скрытый
        self.wih += self.lr * np.dot((hidden_errors * hidden_outputs * (1.0 - hidden_outputs)), np.transpose(inputs))

        pass


    #опрос сети
    def query(self, inputs_list):
        #список входных значений в в двуменрый масив
        inputs=np.array(inputs_list, ndim=2).T

        #расчитываем входящие сигналы для скрытого слоя
        hidden_inputs=np.dot(self.whi, inputs)
        #исходящие сигналы для скрытого слоя
        hidden_outputs=self.activation_func(hidden_inputs)

        #входящие сигналя для выходного слоя
        final_inputs=np.dot(self.who, hidden_outputs)
        #исходящие синалы для выходного слоя
        final_outputs=self.activation_func(final_inputs)

        return final_outputs
        pass

input_nodes=3
output_nodes=3
hidden_nodes=3

learning_rate=0.3

n=neuralNetwork(input_nodes,output_nodes,hidden_nodes,learning_rate)
