import numpy
import scipy.special
import random


#neural network class definition
class neuralNetwork:
    
    #initialize the neural network
    def __init__(self, inputnodes, hidden, outputnodes, learningrate):
        #set number of nodes in each input, hidden, output layer 
        self.inodes = inputnodes
        self.hnode = hidden
        self.onodes = outputnodes

        #가중치 행렬 wih(input_hidden)와 who(hidden_output)

        self.wih = numpy.random.randn(self.hnode, self.inodes)
        print(self.wih[0][0])
        self.who = numpy.random.randn(self.onodes, self.hnode)
        print(self.who[0][0])

        #learning rate
        self.lr = learningrate

        #시그모이드 활성화 함수
        self.activation_function = lambda x: scipy.special.expit(x)
        #Relu 활성화 함수
        self.Relu_func = lambda x : numpy.maximum(0,x)
        #softmax 활성화 함수
        self.softmax_func = lambda x: self.softmax(x)

    def softmax(self, x):
        c = numpy.max(x)
        exp_a = numpy.exp(x-c)
        sum_exp_a = numpy.sum(exp_a)
        y = exp_a / sum_exp_a

        return y

    #신경망 학습시키기
    def train(self, input_list, targets_list):
        # 입력 리스트를 2차원 행렬로 변환
        inputs = numpy.array(inputs_list, ndmin=2).T
        targets = numpy.array(targets_list, ndmin=2).T
        
        # 은닉 계층으로 들어오는 신호를 계산
        hidden_inputs = numpy.dot(self.wih, inputs)
        # 은닉 계층으로 나가는 신호를 계산
        hidden_outputs = self.activation_function(hidden_inputs)
        # 최종 출력 계층으로 들어오는 신호를 계산
        final_inputs = numpy.dot(self.who, hidden_outputs) 
        # 최종 출력 계층으로 나가는 신호를 계산
        final_outputs = self.activation_function(final_inputs)
        
        # 출력계층의 오차는 (실제 값 - 계산 값)
        output_errors = targets - final_outputs
        # 은닉 계층의 오차는 가중치에 의해 나뉜 출력 계층의 오차들을 재조합해 계산
        hidden_errors = numpy.dot(self.who.T, output_errors)
        
        # 은닉 계층과 출력 계층 간의 가중치 업데이트
        self.who += self.lr * numpy.dot((output_errors * final_outputs * (1.0 - final_outputs)), numpy.transpose(hidden_outputs))      
        # 입력 계층과 은닉 계층간의 가중치 업데이트
        self.wih += self.lr * numpy.dot((hidden_errors * hidden_outputs * (1.0 - hidden_outputs)), numpy.transpose(inputs))

    #신경망에 질의하기
    def query(self, inputs_list):
        #입력 리스트를 2차원 행렬로 변환
        inputs = numpy.array(inputs_list, ndmin=2).T
        #1차 은닉 계층으로 들어오는 신호를 계산
        hidden_inputs = numpy.dot(self.wih, inputs)
        #1차 은닉 계층에서 나가는 신호를 계산
        hidden_outputs = self.Relu_func(hidden_inputs)
        #최종 출력 계층으로 들어오는 신호 계산 
        final_inputs = numpy.dot(self.who, hidden_outputs)
        #최종 출력 계층에서 나가는 신호 계산 
        final_outputs = numpy.round(self.softmax_func(final_inputs),15)

      return final_outputs