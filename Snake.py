import pygame
import time
import random
from datetime import datetime
from datetime import timedelta
import math

from pygame.constants import NOEVENT
import NeuralNet as NL

#게임 시스템
class Game_System:

    def __init__(self):
        #게임 종료 체크 변수
        self.done = False
        #점수
        self.score = 0
        self.best_score = 0
        self.best_score_weight = list()
        #폰트
        self.font = pygame.font.SysFont('OpenSans', 30)
        self.font_exit = pygame.font.SysFont('OpenSans',25)
        #재시작 횟수
        self.count = 0
        #무한 반복 방지 제약 생명
        self.life = 1000
        #시간 관련 변수
        self.last_moved_time = datetime.now()
        #배경색
        self.BLACK = (0,0,0)
        #snake색
        self.WHITE = (255,255,255)
        #apple색
        self.RED = (255,0,0)
        #화면 설정
        self.screen = pygame.display.set_mode([850,668])
        self.clock = pygame.time.Clock()
        #키보드 입력값 딕셔너리
        self.KEY_DIRECTION = {
            pygame.K_UP: 'U',
            pygame.K_DOWN: 'D',
            pygame.K_LEFT: 'L',
            pygame.K_RIGHT: 'R',
            pygame.K_ESCAPE: 'Q'
        }
        #신경망 출력값 딕셔너리
        self.KEY_OUTPUT = {
            0:"U",
            1:"D",
            2:"L",
            3:"R"
        }

     
    def draw_block(self, screen, color, position):
        block = pygame.Rect((position[0], position[1]), (20, 20))
        pygame.draw.rect(screen, color, block)
    
    def gameover(self,mode=None):
        time.sleep(1)
        self.count += 1
        self.life = 1000
        self.score = 0
        self.done = False

        runGame(mode)  
    
    




class Snake(Game_System):
    
    def __init__(self):
        super().__init__()
        self.positions = [(4+308,6+308),(26+308,6+308),(48+308,6+308)]
        self.direction = "D"
        self.distnaceApple = []
        self.distnaceWall = []
        self.distanceBody = []

    def draw(self):
        for position in self.positions:
            self.draw_block(self.screen, self.WHITE, position)
    
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
    
    def grow(self):
        tail_position1 = self.positions[-1]
        tail_position2 = self.positions[-2]
        x, y = [tail_position1[i] - tail_position2[i] for i in range(len(tail_position1))]
        self.positions.append((tail_position1[0]+x,tail_position1[1]+y))

    def apple_Distance(self, app_pos):
        self.distnaceApple = []
        for mode in range(1,9):
            self.Distance(mode = mode,apple=app_pos)
        return self.distnaceApple
    
    def wall_Distance(self):
        self.distnaceWall = []
        for mode in range(1,9):
            self.Distance(mode=mode,wall="wall")
        return self.distnaceWall

    def body_Distance(self):
        self.distanceBody = []
        for mode in range(1,9):
            self.Distance(mode=mode,body="body")
        return self.distanceBody

    def Distance(self, mode, apple = None, wall = None, body = None):
        head_position = self.positions[0]
        x1, y1 = head_position
        if apple != None:
            x2, y2 = apple
        #1(x-,y+)
        #2(x-,y)
        #3(x-,y-)
        #4(x,y-)
        #5(x+,y-)
        #6(x+,y)
        #7(x+,y+)
        #8(x,y+)
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
            #apple list
            if apple != None:
                if (x1 == x2 and y1 == y2):
                    self.distnaceApple.append(int(math.sqrt(pow(x2-head_position[0],2)+pow(y2-head_position[1],2))))
                    break
                elif (x1 <= -1 or x1 >= 644) or (y1 <= -1 or y1 >= 646):
                    self.distnaceApple.append(0)
                    break
            elif wall != None:
                if (x1 <= -1 or x1 >= 644) or (y1 <= -1 or y1 >= 646):
                    self.distnaceWall.append(int(math.sqrt(pow(x1-head_position[0],2)+pow(y1-head_position[1],2))))
                    break
            elif body != None:
                if ((x1,y1) in self.positions[1:]):
                    self.distanceBody.append(int(math.sqrt(pow(x1-head_position[0],2)+pow(y1-head_position[1],2))))
                    break
                elif (x1 <= -1 or x1 >= 644) or (y1 <= -1 or y1 >= 646):
                    self.distanceBody.append(0)
                    break

class Apple(Game_System):
    def __init__(self,position = ((random.randint(0,30)*22)+4,(random.randint(0,30)*22)+6)):
        super().__init__()
        self.position = position
    def draw(self):
        self.draw_block(self.screen,self.RED,self.position)

def runGame(mode = None):
    
    pygame.init()

    sys = Game_System()
    snake = Snake()
    apple = Apple()

    output = None
    key = None

    brain = NL.neuralNetwork(24,12,12,4,0.5)

    while not sys.done:
        sys.clock.tick(60)
        sys.screen.fill(sys.BLACK)

        snake_head = snake.positions[0]

        #테두리
        pygame.draw.rect(sys.screen,sys.WHITE,[0,2,664,666],2)

        #점수 표시
        sys.screen.blit(sys.font.render("score : "+str(sys.score),False,sys.WHITE),(700,40))
        sys.screen.blit(sys.font.render("life : "+str(sys.life),False,sys.WHITE),(700,80))
        sys.screen.blit(sys.font.render("count : "+str(sys.count),False,sys.WHITE),(700,120))
        sys.screen.blit(sys.font_exit.render("Press ESC to EXIT",False,sys.WHITE),(685,600))

        if output != None:
            key = output.index(max(output))

        if (snake_head in snake.positions[1:]):
            sys.gameover(mode)
            break

        for event in pygame.event.get():
            #게임 종료
            if event.type == pygame.QUIT:
                sys.done=True
            #키보드 조작시 사용
            if mode != None:
                if event.type == pygame.KEYDOWN:
                    if event.key in sys.KEY_DIRECTION:
                        if sys.KEY_DIRECTION[event.key] == "Q":
                            exit()
                        if sys.KEY_DIRECTION[event.key] == "U" and snake.direction != 'D':
                            snake.direction = sys.KEY_DIRECTION[event.key]
                        elif sys.KEY_DIRECTION[event.key] == "D" and snake.direction != 'U':
                            snake.direction = sys.KEY_DIRECTION[event.key]
                        elif sys.KEY_DIRECTION[event.key] == "L" and snake.direction != 'R':
                            snake.direction = sys.KEY_DIRECTION[event.key]
                        elif sys.KEY_DIRECTION[event.key] == "R" and snake.direction != 'L':
                            snake.direction = sys.KEY_DIRECTION[event.key]
            else :
                if key != None and snake.direction != sys.KEY_OUTPUT[key]:
                    if sys.KEY_OUTPUT[key] == "U" and snake.direction != "D":
                        snake.direction = sys.KEY_OUTPUT[key]
                    elif sys.KEY_OUTPUT[key] == "D" and snake.direction != "U":
                        snake.direction = sys.KEY_OUTPUT[key]
                    elif sys.KEY_OUTPUT[key] == "L" and snake.direction != "R":
                        snake.direction = sys.KEY_OUTPUT[key]
                    elif sys.KEY_OUTPUT[key] == "R" and snake.direction != "L":
                        snake.direction = sys.KEY_OUTPUT[key]
        
        if timedelta(seconds=0.075) <= datetime.now() - sys.last_moved_time:
            snake.move()
            snake.apple_Distance(apple.position)
            snake.wall_Distance()
            snake.body_Distance()
            if len(snake.distnaceApple+snake.distnaceWall+snake.distanceBody) == 24:
                output = list(brain.query(snake.distnaceApple+snake.distnaceWall+snake.distanceBody))
            sys.last_moved_time = datetime.now()

        if snake_head == apple.position:
            sys.score += 1  
            snake.grow()
            while True:
                new_position = ((random.randint(0,30)*22)+4,(random.randint(0,30)*22)+6)
                if not(new_position in snake.positions) and (new_position[0] >= 4 and new_position[0] < 664) and (new_position[1] >= 6 and new_position[1] < 666):
                    apple.position = new_position
                    break
        if (snake_head[0] <= -1 or snake_head[0] >= 644) or (snake_head[1] <= -1 or snake_head[1] >= 646):
            sys.gameover(mode)
            break

        snake.draw()
        apple.draw()
        pygame.display.flip()

        if sys.life <= 0:
            sys.gameover(mode)
            break
        else : sys.life -= 1


if __name__ == "__main__":
    runGame(1)