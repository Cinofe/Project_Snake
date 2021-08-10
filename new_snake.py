import pygame as pg
import numpy, time, math, random
from datetime import datetime, timedelta


class Environment:
    def __init__(self):
        pg.init()
        #색
        self.backGround = (0,0,0)
        self.WHITE = (255,255,255)
        #   시스템
        #종료 체크
        self.done = False
        #폰트
        self.font = pg.font.SysFont('OpenSans', 30)
        self.font_exit = pg.font.SysFont('OpenSans',25)
        #남은 이동수
        self.life = 1000
        #마지막 이동 시간
        self.last_moved_time = datetime.now()
        #화면 표시 설정
        self.screen = pg.display.set_mode([850,668])
        #fps
        self.clock = pg.time.Clock()
        #입력값 대비 이동 방향
        self.KEY_OUTPUT = {0:"U",1:"D",2:"L",3:"R"}
        #점수와 반복 횟수
        self.score = 0
        self.count = 0

    #화면 업데이트
    def screenUpdate(self):
        #60fps
        self.clock.tick(60)
        #배경 채우기(검정)
        self.screen.fill(self.backGround)
        #테두리 만들기(하양,두께 2)
        pg.draw.rect(self.screen,self.WHITE,[0,2,664,666],2)
        #각 점수, 남은 이동수, 반복 횟수, 종료키 안내 문자 표시
        self.screen.blit(self.font.render("score : "+str(self.score),False,self.WHITE),(700,40))
        self.screen.blit(self.font.render("life : "+str(self.life),False,self.WHITE),(700,80))
        self.screen.blit(self.font.render("count : "+str(self.count),False,self.WHITE),(700,120))
        self.screen.blit(self.font_exit.render("Press ESC to EXIT",False,self.WHITE),(685,600))
        #pygame 화면 업데이트
        pg.display.flip()
    #그리기
    def draw_block(self, position, color):
        block = pg.Rect((position[0], position[1]), (20, 20))
        pg.draw.rect(self.screen, color, block)



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
    def draw(self, Env):
        for position in self.positions:
            Env.draw_block(position, self.snakeColor)
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
    #음식과의 거리
    def food_Distance(self, app_pos):
        #기존 거리값 초기화
        self.distnaceFood = []
        #몸통의 머리로 부터 8방향 체크
        for mode in range(1,9):
            self.Distance(mode = mode,food=app_pos)
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

if __name__ == "__main__":
    env = Environment()
    snake = Snake()

    while True:
        env.screenUpdate()
