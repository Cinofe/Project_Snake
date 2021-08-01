import numpy
import scipy.special
import random


#neural network class definition
class neuralNetwork:
    
    #initialize the neural network
    def __init__(self, inputnodes, hidden1, hidden2, outputnodes, learningrate):
        #set number of nodes in each input, hidden, output layer 
        self.inodes = inputnodes
        self.hnode1 = hidden1
        self.hnode2 = hidden2
        self.onodes = outputnodes

        #가중치 행렬 wih(input_hidden)와 who(hidden_output)
        #배열 내 가중치는 w_i_j로 표기. 노드 i에서 다음 계층의 노드 j로 연결됨을 의미
        #w11 w21
        #w12 w22

        self.wih = numpy.random.normal(0.0, pow(self.hnode1, - 0.5),(self.hnode1, self.inodes))
        self.whh = numpy.random.normal(0.0, pow(self.hnode2, - 0.5),(self.hnode2, self.hnode1))
        self.who = numpy.random.normal(0.0, pow(self.onodes, - 0.5),(self.onodes, self.hnode2))

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
    def train(self):
        pass

    #신경망에 질의하기
    def query(self, inputs_list):
      #입력 리스트를 2차원 행렬로 변환
      inputs = numpy.array(inputs_list, ndmin=2).T
      #1차 은닉 계층으로 들어오는 신호를 계산
      hidden1_inputs = numpy.dot(self.wih, inputs)
      #1차 은닉 계층에서 나가는 신호를 계산
      hidden1_outputs = self.activation_function(hidden1_inputs)
      #2차 은닉 계층으로 들어오는 신호를 계산
      hidden2_inputs = numpy.dot(self.whh,hidden1_outputs)
      #2차 은닉 계층에서 나가는 신호를 계산
      hidden2_outputs = self.Relu_func(hidden2_inputs)
      #최종 출력 계층으로 들어오는 신호 계산 
      final_inputs = numpy.dot(self.who, hidden2_outputs)
      #최종 출력 계층에서 나가는 신호 계산 
      final_outputs = numpy.round(self.softmax_func(final_inputs),15)

      return final_outputs