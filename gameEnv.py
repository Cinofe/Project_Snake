from datetime import datetime
import pygame as pg

#게임 시스템
class Env:
    def __init__(self):
        pg.init()
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
        # Loss
        self.Loss = 0

    #화면 업데이트
    def screenUpdate(self,snake, food, env):
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
        self.screen.blit(self.font.render("Loss : "+str(self.Loss),False,self.WHITE),(680,180))
        self.screen.blit(self.font_exit.render("Press ESC to EXIT",False,self.WHITE),(685,600))

        #뱀 그리기
        snake.draw(env)
        #먹이 그리기
        food.draw(env)
        #pygame 화면 업데이트
        pg.display.flip()

    #그리기
    def draw_block(self, position, color):
        block = pg.Rect((position[0], position[1]), (20, 20))
        pg.draw.rect(self.screen, color, block)

    #입력키 체크
    def keyCheck(self,snake, key=None,mode=None):
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
    def resultCheck(self,snake, result):
        if result == 0 and snake.direction != 'D':
            snake.direction = 'U'
        elif result == 1 and snake.direction != 'U':
            snake.direction = 'D'
        elif result == 2 and snake.direction != 'R':
            snake.direction = 'L'
        elif result == 3 and snake.direction != 'L':
            snake.direction = 'R'
    
    #종료 체크
    def isDone(self,snake):
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