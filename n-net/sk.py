import numpy as np
import matplotlib.pyplot as mpl
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

    def train(self, inputs_list,targets_list):
        # ыходные значения в двумерный масив
        inputs = np.array(inputs_list, ndmin=2).T
        targets = np.array(targets_list, ndmin=2).T

        # расчёт входящих сигналов для скрытово слоя
        hidden_inputs = np.dot(self.wih, inputs)
        # сигнал  исходящие для скрытого слоя
        hidden_outputs = self.activation_func(hidden_inputs)

        # входящие для выходного слоя
        final_inputs = np.dot(self.who, hidden_outputs)
        # исходящие для выходного слоя
        final_outputs = self.activation_func(final_inputs)
        # ошибки выходного слоя (целевое знач. - фактическое знач.)
        output_errors = targets - final_outputs
        # ошибки скрытого слоя распределения пропорционально коэфицентам связей и рекомбинирование на скрытых узлах
        hidden_errors = np.dot(self.who.T, output_errors)

        # обновление весов связей слоёв скрытый--выходной
        self.who += self.lr * np.dot((output_errors * final_outputs * (1.0 - final_outputs)), np.transpose(hidden_outputs))

        # обновление весов связей слоёв выходной--скрытый
        self.wih += self.lr * np.dot((hidden_errors * hidden_outputs * (1.0 - hidden_outputs)), np.transpose(inputs))

        pass


    #опрос сети
    def query(self, inputs_list):
        #список входных значений в в двуменрый масив
        inputs=np.array(inputs_list, ndmin=2).T

        #расчитываем входящие сигналы для скрытого слоя
        hidden_inputs=np.dot(self.wih, inputs)
        #исходящие сигналы для скрытого слоя
        hidden_outputs=self.activation_func(hidden_inputs)

        #входящие сигналя для выходного слоя
        final_inputs=np.dot(self.who, hidden_outputs)
        #исходящие синалы для выходного слоя
        final_outputs=self.activation_func(final_inputs)

        return final_outputs


input_nodes=784
hidden_nodes=100
output_nodes=10


learning_rate=0.3

n=neuralNetwork(input_nodes,hidden_nodes,output_nodes,learning_rate)

training_data_file=open("mnist_dataset/mnist_train_100.csv", 'r')
training_data_list=training_data_file.readlines()
training_data_file.close()


# train the neural network

# epochs is the number of times the training data set is used for training
epochs = 5

for e in range(epochs):
    # go through all records in the training data set
    for record in training_data_list:
        # split the record by the ',' commas
        all_values = record.split(',')
        # scale and shift the inputs
        inputs = (np.asfarray(all_values[1:]) / 255.0 * 0.99) + 0.01
        # create the target output values (all 0.01, except the desired label which is 0.99)
        targets = np.zeros(output_nodes) + 0.01
        # all_values[0] is the target label for this record
        targets[int(all_values[0])] = 0.99
        n.train(inputs, targets)
        pass
    pass


test_data_file=open("mnist_dataset/mnist_test_10.csv", 'r')
test_data_list=test_data_file.readlines()
test_data_file.close()

test_value=test_data_list[7].split(',')
print(test_value[0])

test_array=(np.asfarray(test_value[1:]).reshape(28,28))
#mpl.imshow(test_array, cmap="Greys", interpolation='None')
#mpl.show()

print(n.query((np.asfarray(test_value[1:])/255.0*0.99)+0.01))
