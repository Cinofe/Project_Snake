import numpy as np
from scipy import special

class NeuralNet:
    def __init__(self,iSize,hSize,oSize):
        #레이어들
        self.iLayer = []
        self.h1Layer = []
        self.h2Layer = []
        self.oLayer = []
        #가중치 최초 가중치는 -1~1 사이의 랜덤값
        self.Wi = np.random.uniform(-1,1,(iSize,hSize))
        self.Wh = np.random.uniform(-1,1,(hSize,hSize))
        self.Wo = np.random.uniform(-1,1,(hSize,oSize))

        #시그모이드 활성화 함수
        self.activation_function = lambda x: special.expit(x)
        #Relu 활성화 함수
        self.Relu_func = lambda x : np.maximum(0,x)
        #softmax 활성화 함수
        self.softmax_func = lambda x: self.softmax(x)
    #softmax 활성화 함수
    def softmax(self, x):
        c = np.max(x)
        exp_a = np.exp(x-c)
        sum_exp_a = np.sum(exp_a)
        y = exp_a / sum_exp_a

        return y
    #다음 이동 연산하는 함수(생각하는 함수)
    def query(self, inputLayer):
        #들어온 입력
        self.iLayer = np.array(inputLayer)
        #입력에서 1차 히든 레이어 연산
        self.h1Layer = np.dot(self.iLayer,self.Wi)
        #1차 히든 레이어에서 2차 히든 레이어로 출력 하는 값
        self.h1Layer = self.activation_function(self.h1Layer)
        #2차 히든 레이어 연산
        self.h2Layer = np.dot(self.h1Layer,self.Wh)
        #2차 히든 레이어 에서 출력 레이어로 출력 하는 값
        self.h2Layer = self.activation_function(self.h2Layer)
        #출력 레이어 연산
        self.oLayer = np.dot(self.h2Layer,self.Wo)
        #마지막 출력 연산
        self.oLayer = self.softmax_func(self.oLayer)

        return list(self.oLayer)