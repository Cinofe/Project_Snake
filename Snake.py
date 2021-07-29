import pygame
from datetime import datetime
from datetime import timedelta


#pygame 초기화
pygame.init()

#화면 크기
size = [800,800]

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

#블럭 생성 함수

positions = [(0,2),(0,1),(0,0)]
i = 1
x, y = 0, 0

while not done:
    for event in pygame.event.get():# User did something
        if event.type == pygame.QUIT:# If user clicked close
            done=True # Flag that we are done so we exit this loop
    if timedelta(seconds=0.1) <= datetime.now() - last_moved_time:
        block = pygame.Rect((x,y),(20,20))
        pygame.draw.rect(screen,WHITE,block)
        last_moved_time = datetime.now()
        x += 22

    pygame.display.flip()



'''
if timedelta(seconds=0.1) <= datetime.now() - last_moved_time:
            snake.move()
            last_moved_time = datetime.now()
'''