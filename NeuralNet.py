import numpy as np
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
        self.weightin = []
        self.weighthi = []
        self.weightou = []

        #가중치 행렬 wih(input_hidden)와 who(hidden_output)
        if len(self.weight1) == 0 or len(self.weight2) == 0:
            self.wih = np.random.randn(self.hnode, self.inodes)
            self.who = np.random.randn(self.onodes, self.hnode)
        else :
            np.reshape(self.weight1,1)
            np.reshape(self.weight2,1)
            for _ in range(len(self.weight1)):
                if self.weight1 == self.weight2:
                    self.weight.append(self.weight1)
                else : 
                    self.weight.append(np.random.randn(1)[0])
            
            self.wih = np.reshape(self.weight1,(self.hnode, self.inodes))
            self.who = np.reshape(self.weight2,(self.onodes, self.hnode))

        #learning rate
        self.lr = learningrate

        #시그모이드 활성화 함수
        self.activation_function = lambda x: scipy.special.expit(x)
        #Relu 활성화 함수
        self.Relu_func = lambda x : np.maximum(0,x)
        #softmax 활성화 함수
        self.softmax_func = lambda x: self.softmax(x)

    def softmax(self, x):
        c = np.max(x)
        exp_a = np.exp(x-c)
        sum_exp_a = np.sum(exp_a)
        y = exp_a / sum_exp_a

        return y

    #신경망 학습시키기
    def CrossOver(self, w1,w2):
        pass

    #신경망에 질의하기
    def query(self, inputs_list):
        #입력 리스트를 2차원 행렬로 변환
        inputs = np.array(inputs_list, ndmin=2).T
        #1차 은닉 계층으로 들어오는 신호를 계산
        hidden_inputs = np.dot(self.wih, inputs)
        #1차 은닉 계층에서 나가는 신호를 계산
        hidden_outputs = self.Relu_func(hidden_inputs)
        #최종 출력 계층으로 들어오는 신호 계산 
        final_inputs = np.dot(self.who, hidden_outputs)
        #최종 출력 계층에서 나가는 신호 계산 
        final_outputs = np.round(self.softmax_func(final_inputs),15)

        return final_outputs



if __name__ == "__main__":
    wi1 = np.random.randint(0,10,(24,14))
    wi2 = np.random.randint(0,10,(24,14))
    wh1 = np.random.randint(0,10,(14,14))
    wh2 = np.random.randint(0,10,(14,14))
    wo1 = np.random.randint(0,10,(14,4))
    wo2 = np.random.randint(0,10,(14,4))

    nwi = np.zeros((24,14))
    for i in range(len(wi1)):
        for j in range(len(wi1[0])):
            if j < len(wi1[0])/2:
                nwi[i][j] = wi1[i][j]
            else:
                nwi[i][j] = wi2[i][j]
    nwh = np.zeros((14,14))
    for i in range(len(wh1)):
        for j in range(len(wh1[0])):
            if j < len(wh1[0])/2:
                nwh[i][j] = wh1[i][j]
            else:
                nwh[i][j] = wh2[i][j]
    print(nwh)
    wi1 = nwh
    print(wi1)

#리스트에 각 확률의 누적합을 넣어 놓고 랜덤으로 뽑기 이론 틀린듯
#참고
'''
itemList = ["귤", "상추", "레몬", "소다", "꽝"]
possibility = [3, 1, 5, 2.5, 2]
randomNumber = random.random() * sum(possibility)
for i, j in enumerate(itemList):
  if randomNumber > possibility[i]:
    randomNumber -= possibility[i]
  else:
    print(i,j)
    break
'''