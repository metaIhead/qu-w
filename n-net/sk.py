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

        #print(len(self.wih),type(self.wih))
        #print("self.who: ",type(self.who),len(self.who),len(self.who[0]))
        save_wt(self.who,self.wih)

        return final_outputs


def save_wt(array_who,array_wih):
    wih=open("wih.txt", 'w')
    who=open("who.txt", 'w')

    for index in range(len(array_who)):
        for counter in range(len(array_who[index])):
            value=str(array_who[index][counter])
            who.write(value + '\n')

    for index in range(len(array_wih)):
        for counter in range(len(array_wih[index])):
            value=str(array_wih[index][counter])
            wih.write(value + '\n')

    who.close()
    wih.close()
    pass




input_nodes=784
hidden_nodes=10 #100-200
output_nodes=10


learning_rate=0.3

n=neuralNetwork(input_nodes,hidden_nodes,output_nodes,learning_rate)

training_data_file=open("mnist_dataset/mnist_train_100.csv", 'r')
training_data_list=training_data_file.readlines()
training_data_file.close()


# тренировка нейроной сети

#эпоха - кол во тренировок с одним и ем же набором данных
epochs = 5

for e in range(epochs):
    for record in training_data_list:
        all_values = record.split(',')
        # маштабирование и смещение входных значений
        inputs = (np.asfarray(all_values[1:]) / 255.0 * 0.99) + 0.01
        #все целевые значения прюлижаються к 0.01, а маркерное значение к 0.99
        targets = np.zeros(output_nodes) + 0.01
        targets[int(all_values[0])] = 0.99
        #данные уходят на тренровку сети
        n.train(inputs, targets)
        pass
    pass


test_data_file=open("mnist_dataset/mnist_test_10.csv", 'r')
test_data_list=test_data_file.readlines()
test_data_file.close()

test_value=test_data_list[7].split(',')
#print(test_value[0])

test_array=(np.asfarray(test_value[1:]).reshape(28,28))
#mpl.imshow(test_array, cmap="Greys", interpolation='None')
#mpl.show()

n.query((np.asfarray(test_value[1:])/255.0*0.99)+0.01)
