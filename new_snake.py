import pygame as pg
import numpy as np, time, math, random, copy
from scipy import special
from datetime import datetime, timedelta


class Environment:
    def __init__(self):
        pg.init()
        #색
        self.backGround = (0,0,0)
        self.WHITE = (255,255,255)
        #----시스템----
        #종료 체크
        self.done = False
        #폰트
        self.font = pg.font.SysFont('OpenSans', 30)
        self.font_exit = pg.font.SysFont('OpenSans',25)
        #남은 이동수
        self.life = 400
        #마지막 이동 시간
        self.last_moved_time = datetime.now()
        self.last_moved_time2 = datetime.now()
        #화면 표시 설정
        self.screen = pg.display.set_mode([850,668])
        #fps
        self.clock = pg.time.Clock()
        #입력값 대비 이동 방향
        self.KEY_OUTPUT = {0:"U",1:"D",2:"L",3:"R"}
        #점수와 반복 횟수
        self.score = 0
        self.bestScore = 0
        self.count = 0
        #진화 횟수
        self.generation = 0

    #화면 업데이트
    def screenUpdate(self):
        #60fps
        self.clock.tick(60)
        #배경 채우기(검정)
        self.screen.fill(self.backGround)
        #테두리 만들기(하양,두께 2)
        pg.draw.rect(self.screen,self.WHITE,[0,2,664,666],2)
        #각 점수, 남은 이동수, 반복 횟수, 종료키 안내 문자 표시
        self.screen.blit(self.font.render("score : "+str(self.score),False,self.WHITE),(680,20))
        self.screen.blit(self.font.render('best score : '+str(self.bestScore),False,self.WHITE),(680,60))
        self.screen.blit(self.font.render("life : "+str(self.life),False,self.WHITE),(680,100))
        self.screen.blit(self.font.render("count : "+str(self.count),False,self.WHITE),(680,140))
        self.screen.blit(self.font.render("Generation : "+str(self.generation),False,self.WHITE),(680,180))
        self.screen.blit(self.font_exit.render("Press ESC to EXIT",False,self.WHITE),(685,600))

        #뱀 그리기
        snake.draw()
        #먹이 그리기
        food.draw()   
        #pygame 화면 업데이트
        pg.display.flip()

    #그리기
    def draw_block(self, position, color):
        block = pg.Rect((position[0], position[1]), (20, 20))
        pg.draw.rect(self.screen, color, block)

    #입력키 체크
    def keyCheck(self,key=None,mode=None):
        if key == pg.K_ESCAPE:
            self.done = True
            return True
        if mode == 1:
            if key == pg.K_UP and snake.direction != 'D':
                snake.direction = 'U'
            elif key == pg.K_DOWN and snake.direction != 'U':
                snake.direction = 'D'
            elif key == pg.K_LEFT and snake.direction != 'R':
                snake.direction = 'L'
            elif key == pg.K_RIGHT and snake.direction != 'L':
                snake.direction = 'R'
        return False

    #brain 연산 출력 값 체크
    def resultCheck(self, result):
        if result == 0 and snake.direction != 'D':
            snake.direction = 'U'
        elif result == 1 and snake.direction != 'U':
            snake.direction = 'D'
        elif result == 2 and snake.direction != 'R':
            snake.direction = 'L'
        elif result == 3 and snake.direction != 'L':
            snake.direction = 'R'
    
    #종료 체크
    def isDone(self):
        if self.life <= 0:
            self.done = True
        if (snake.positions[0][0] <= -1 or
             snake.positions[0][0] >= 644 or
             snake.positions[0][1] <= -1 or
             snake.positions[0][1] >= 646):
            self.done = True

    #신기록 체크
    def isBest(self):
        if self.score > self.bestScore:
            return True
        else : return False
    #초기화
    def reset(self):
        self.done = False
        self.life = 400
        self.score = 0
        self.last_moved_time2 = datetime.now()

class Snake:
    def __init__(self):
        #색(하양)
        self.snakeColor = (255,255,255)
        #snake 좌표
        self.positions = [(4+308,6+308),(26+308,6+308),(48+308,6+308)]
        #진행 방향
        self.direction = "D"
        #각 음식, 벽, 몸통과의 거리
        self.distnaceFood = []
        self.distnaceWall = []
        self.distanceBody = []
    #몸통 그리기
    def draw(self):
        for position in self.positions:
            env.draw_block(position, self.snakeColor)
    #이동하기
    def move(self):
        head_positon = self.positions[0]
        x,y = head_positon
        if self.direction == "U":
            self.positions.insert(0,(x, y-22))
            del(self.positions[-1:])
        elif self.direction == "D":
            self.positions.insert(0,(x, y+22))
            del(self.positions[-1:])
        elif self.direction == "L":
            self.positions.insert(0,(x-22, y))
            del(self.positions[-1:])
        elif self.direction == "R":
            self.positions.insert(0,(x+22, y))
            del(self.positions[-1:])
    #음식 먹었을 경우 성장
    def grow(self):
        #몸통의 끝에서 첫번째 두번째 좌표를 가져옴
        tail_position1 = self.positions[-1]
        tail_position2 = self.positions[-2]
        #첫번째 좌표에서 두번째 좌표를 뺀 값(진행 방향을 알기위해)을
        x, y = [tail_position1[i] - tail_position2[i] for i in range(len(tail_position1))]
        #끝에서 첫번째 좌표와 합해서 새로운 몸통을 형성(꼬리의 진행방향과 같은곳에 생성됨)
        self.positions.append((tail_position1[0]+x,tail_position1[1]+y))
        #음식을 먹었을 경우 남은 이동 수 증가와 점수 증가
        env.life += 50
        env.score += 1
    #음식과의 거리
    def food_Distance(self, food_pos):
        #기존 거리값 초기화
        self.distnaceFood = []
        #몸통의 머리로 부터 8방향 체크
        for mode in range(1,9):
            self.Distance(mode = mode,food=food_pos)
        return self.distnaceFood
    #벽과의 거리
    def wall_Distance(self):
        #기존 거리값 초기화
        self.distnaceWall = []
        #몸통의 머리로 부터 8방향 체크
        for mode in range(1,9):
            self.Distance(mode=mode,wall="wall")
        return self.distnaceWall
    #몸통과의 거리
    def body_Distance(self):
        #기존 거리값 초기화
        self.distanceBody = []
        #몸통의 머리로 부터 8방향 체크
        for mode in range(1,9):
            self.Distance(mode=mode,body="body")
        return self.distanceBody
    #거리측정 함수
    # 파라미터로 food의 값이 들어오면 food과의 거리 측정,
    # wall의 값이 들어오면 wall과의 거리측정,
    # body도 마찬가지
    def Distance(self, mode, food = None, wall = None, body = None):
        #몸통의 머리 좌표 가져오기
        head_position = self.positions[0]
        x1, y1 = head_position
        if food != None:
            x2, y2 = food
        #29번 반복(화면의 가로세로 칸이 29칸)
        for _ in range(30):
            if mode == 1:
                x1 -= 22
                y1 += 22
            elif mode == 2:
                x1 -= 22
            elif mode == 3:
                x1 -= 22
                y1 -= 22
            elif mode == 4:
                y1 -= 22
            elif mode == 5:
                x1 += 22
                y1 -= 22
            elif mode == 6:
                x1 += 22
            elif mode == 7:
                x1 += 22
                y1 += 22
            elif mode == 8:
                y1 += 22
            #food list
            if food != None:
                if (x1 == x2 and y1 == y2):
                    #점과 점 사이의 거리 구하는 공식 사용(root((x2-x1)^2+(y2-y1)^2))
                    self.distnaceFood.append(int(math.sqrt(pow(x2-head_position[0],2)+pow(y2-head_position[1],2))))
                    break
                elif (x1 <= -1 or x1 >= 644) or (y1 <= -1 or y1 >= 646):
                    #결과값이 테두리를 벗어날 경우 0입력
                    self.distnaceFood.append(0)
                    break
            elif wall != None:
                if (x1 <= -1 or x1 >= 644) or (y1 <= -1 or y1 >= 646):
                    #테두리와 좌표 거리 구하는 공식 사용
                    self.distnaceWall.append(int(math.sqrt(pow(x1-head_position[0],2)+pow(y1-head_position[1],2))))
                    break
            elif body != None:
                #좌표가 몸통 리스트에 포함되면 True 반환
                if ((x1,y1) in self.positions[1:]):
                    #몸통과 거리 구하는 공식 사용
                    self.distanceBody.append(int(math.sqrt(pow(x1-head_position[0],2)+pow(y1-head_position[1],2))))
                    break
                elif (x1 <= -1 or x1 >= 644) or (y1 <= -1 or y1 >= 646):
                    #테두리를 벗어날 경우 0 입력
                    self.distanceBody.append(0)
                    break

class Food:
    def __init__(self):
        #색(빨강)
        self.foodColor = (255,0,0)
        #매번 좌표는 랜덤으로 부여
        self.pos = ((random.randint(0,29)*22)+4,(random.randint(0,29)*22)+6)
    
    def draw(self):
        env.draw_block(self.pos,self.foodColor)
    
    def relocation(self):
        self.pos = ((random.randint(0,29)*22)+4,(random.randint(0,29)*22)+6)
        while self.pos in snake.positions:
            self.pos = ((random.randint(0,29)*22)+4,(random.randint(0,29)*22)+6)

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
#
class DNA:
    def __init__(self):
        self.clones = []
        self.scores = []
        self.probs = [0]
        self.parents = []
        self.count = 0

    def append(self, dna):
        if len(self.clones) < 10:
            self.clones.append(copy.deepcopy(brain))
            self.scores.append(env.score)
        elif len(self.clones) == 10:
            sum = np.cumsum(self.scores)
            ran = round(random.uniform(0,1),2)
            for i in range(1,len(self.clones)):
                self.probs.append(round((self.scores[i]/sum[-1])+self.probs[i-1],1))
            self.probs.append(1)
            for _ in range(2):
                for i in range(len(self.probs)):
                    if ran >= self.probs[i-1] and ran <= self.probs[i]:
                        self.parents.append(self.clones[i])
            
            if random.randint(0,10000) <= 10:
                self.mutate()
            
            self.crossOver()

    def mutate(self):
        pass

    def crossOver(self):
        i = 0
        j = 0
        while i < len(brain.Wi):
            while j < len(brain.Wi[0]):
                if random.randint(0,100) >= 49:
                    brain.Wi[i][j] = self.clones[0].Wi[i][j]
                    j += 1
                else:
                    brain.Wi[i][j] = self.clones[1].Wi[i][j]
                    j += 1
            i += 1
        i = 0
        j = 0
        while i < len(brain.Wh):
            while j < len(brain.Wh[0]):
                if random.randint(0,100) >= 49:
                    brain.Wh[i][j] = self.clones[0].Wh[i][j]
                    j += 1
                else:
                    brain.Wh[i][j] = self.clones[1].Wh[i][j]
                    j += 1
            i += 1
        i = 0
        j = 0
        while i < len(brain.Wo):
            while j < len(brain.Wo[0]):
                if random.randint(0,100) >= 49:
                    brain.Wo[i][j] = self.clones[0].Wo[i][j]
                    j += 1
                else:
                    brain.Wo[i][j] = self.clones[1].Wo[i][j]
                    j += 1
            i += 1
        self.clone1 = None
        self.clone2 = None
        env.generation += 1

if __name__ == "__main__":
    env = Environment()
    brain = NeuralNet(24,14,4)
    dna = DNA()
    #반복 횟수
    epoch = 500
    #모드 설정(0:ai, 1:user)
    mode = 0

    while epoch > 0:
        env.reset()
        snake = Snake()
        food = Food()
        #매 반복마다 진화가 없다면 brain을 새로 생성
        if env.generation == 0:
            brain = NeuralNet(24,14,4)

        while True:
            #화면 구성 업데이트
            env.screenUpdate()

            #종료 체크
            env.isDone()
            if env.done:
                env.count += 1
                break
            
            #키보드 입력값 검사
            for event in pg.event.get():
                if event.type == pg.KEYDOWN:
                    #키보드 입력값 체크
                    if env.keyCheck(event.key,mode=mode):
                        epoch = 0
                        break
            if timedelta(seconds=2) <= datetime.now() - env.last_moved_time2:
                env.score += 1
                env.last_moved_time2 = datetime.now()
            #second 는 한tick 즉 한 프레임당 시간을 말함 낮을 수록 뱀 이동속도 상승
            #현재 시간과 마지막 이동시간을 비교해서 0.5초 이상 지났을 경우 실행
            if timedelta(seconds=0.075) <= datetime.now() - env.last_moved_time:
                if mode == 0:
                    if env.isBest():
                        dna.append(brain)
                    #brain 반환 값 검사
                    if len(snake.food_Distance(food.pos)+snake.wall_Distance()+snake.body_Distance()) == 24:
                        result = brain.query(snake.food_Distance(food.pos)+snake.wall_Distance()+snake.body_Distance())
                        #이동 방향 설정
                        env.resultCheck(result.index(max(result)))
                #뱀 이동
                snake.move()
                #이동 할 때 마다 남은 이동 수 감소
                env.life -= 1
                #마지막 이동시각 저장
                env.last_moved_time = datetime.now()
            
            #먹이 먹었는지 체크
            if snake.positions[0] == food.pos:
                snake.grow()
                food.relocation()
        epoch -= 1