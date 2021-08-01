import numpy
import scipy.special


#neural network class definition
class neuralNetwork:
    
    #initialize the neural network
    def __init__(self, inputnodes, hiddennodes, outputnodes, learningrate):
        #set number of nodes in each input, hidden, output layer 
        self.inodes = inputnodes
        self.hnodes = hiddennodes
        self.onodes = outputnodes

        #가중치 행렬 wih(input_hidden)와 who(hidden_output)
        #배열 내 가중치는 w_i_j로 표기. 노드 i에서 다음 계층의 노드 j로 연결됨을 의미
        #w11 w21
        #w12 w22

        self.wih = numpy.random.normal(0.0, pow(self.hnodes, - 0.5),(self.hnodes, self.inodes))
        self.who = numpy.random.normal(0.0, pow(self.onodes, - 0.5),(self.onodes, self.hnodes))

        #learning rate
        self.lr = learningrate

        #expit()는 시그모이드 함수
        self.activation_function = lambda x: scipy.special.expit(x) 

    #신경망 학습시키기
    def train():
        pass

    #신경망에 질의하기
    def query(self, inputs_list):
      #입력 리스트를 2차원 행렬로 변환
      inputs = numpy.array(inputs_list, ndmin=2).T
      #은닉 계층으로 들어오는 신호를 계산
      hidden_inputs = numpy.dot(self.wih, inputs)
      #은닉 계층에서 나가는 신호를 계산
      hidden_outputs = self.activation_function(hidden_inputs)
      #최종 출력 계층으로 들어오는 신호 계산 
      final_inputs = numpy.dot(self.who, hidden_outputs)
      #최종 출력 계층에서 나가는 신호 계산 
      final_outputs = self.activation_function(final_inputs)
      
      return final_outputs