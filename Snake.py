import pygame
from datetime import datetime
from datetime import timedelta


#pygame 초기화
pygame.init()

#화면 크기
size = [850,664]

#배경색
BLACK = (0,0,0)
#snake색
WHITE = (255,255,255)
#apple색
RED = (255,0,0)

#배경 설정
screen = pygame.display.set_mode(size)

#게임 종료 체크 변수
done = False

#시간 관련 변수
clock = pygame.time.Clock()
last_moved_time = datetime.now()
#테두리
pygame.draw.rect(screen,WHITE,[0,2,660,662],2)

class Game_System:
     
    def draw_block(self, screen, color, position):
        block = pygame.Rect((position[0], position[1]), (20, 20))
        pygame.draw.rect(screen, color, block)


class Snake(Game_System):
    
    def __init__(self):
        self.positions = [(4,6),(26,6)]
        self.direction = ''

    def draw(self):
        for position in self.positions:
            super().draw_block(screen, WHITE, position)


while not done:

    snake = Snake()
    for event in pygame.event.get():# User did something
        print(event)
        if event.type == pygame.QUIT:# If user clicked close
            done=True # Flag that we are done so we exit this loop
    
    if timedelta(seconds=0.1) <= datetime.now() - last_moved_time:
        last_moved_time = datetime.now()

    snake.draw()
    pygame.display.flip()