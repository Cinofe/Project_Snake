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



class Snake:
    def __init__(self):
        #색(하양)
        self.snakeColor = (255,255,255)

class Food:
    def __init__(self):
        #색(빨강)
        self.foodColor = (255,0,0)

if __name__ == "__main__":
    env = Environment()
    snake = Snake()

    while True:
        env.screenUpdate()
