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
        # Learning rate
        self.Lr = 0.0001
    
    # Relu 함수
    def Relu(self, x):
        x = np.clip(x, -1e32, 1e32)
        return np.maximum(0, x)
    
    #softmax 활성화 함수
    def softmax(self, x):
        c = np.max(x)
        exp_a = np.exp(x-c)
        sum_exp_a = np.sum(exp_a)
        y = exp_a / sum_exp_a

        return y
    
    # drop out
    def dropOut(self, x:np.ndarray, prob=0.5):
        return x * (np.random.binomial(1, prob, size=x.shape)/prob)
    
    ## Cross Entropy
    def cross_entropy(self, y, t):
        return -(t * np.log(y + 1e-7))
    
    def train(self, inputs, target):
        output = self.query(inputs)
        target = self.query(target)
        # Loss 계산
        target = np.exp(-np.array(target))

        dError = self.cross_entropy(output, target)

        # 역전파 출력 -> 2차 Hidden
        dh2Layer = np.dot(dError, self.Wo.T)
        self.Wo -= self.Lr * np.dot(self.h2Layer.reshape(-1, 1), dError.reshape(1, -1))

        # 2차 Hidden -> 1차 Hidden
        dh2Layer *= self.Relu(self.h2Layer)
        dh1Layer = np.dot(self.Wh.T, dh2Layer.T)  # self.Wh를 전치하여 사용
        self.Wh -= self.Lr * np.dot(dh2Layer, self.h1Layer.reshape(-1, 1))

        # 1차 Hidden -> input
        dh1Layer *= self.Relu(self.h1Layer)
        self.Wi -= self.Lr * np.dot(self.iLayer.reshape(-1,1), dh1Layer.reshape(1,-1))

        print(self.Wo, self.Wh, self.Wi, self.query(inputs))

    
    #다음 이동 연산하는 함수(생각하는 함수)
    def query(self, inputLayer):
        # 들어온 입력을 0~1 사이 값으로 정규화
        inputLayer = inputLayer / (np.max(inputLayer)+ 1e-6)
        self.iLayer = np.array(inputLayer)
        
        # 입력에서 1차 히든 레이어 연산
        self.h1Layer = np.dot(self.iLayer, self.Wi)
        # 1차 히든 레이어에서 2차 히든 레이어로 출력 하는 값
        self.h1Layer = self.Relu(self.h1Layer)
        # # drop out
        self.h1Layer = self.dropOut(self.h1Layer, 0.5)
        
        #2차 히든 레이어 연산
        self.h2Layer = np.dot(self.h1Layer, self.Wh)
        #2차 히든 레이어 에서 출력 레이어로 출력 하는 값
        self.h2Layer = self.Relu(self.h2Layer)
        # drop Out
        self.h2Layer = self.dropOut(self.h2Layer, 0.5)
        
        #출력 레이어 연산
        self.oLayer = np.dot(self.h2Layer, self.Wo)
        #마지막 출력 연산
        self.oLayer = self.softmax(self.oLayer)

        return self.oLayer
    
# --2023.10 참고 사항
'''
    학습이 이루어 지지 않은 이유
    - 손실함수로 loss를 계산하지 못했고
    - 이를 통한 역전파로 가중치를 업데이트 하지 않아 학습이 이루어지지 않음
'''