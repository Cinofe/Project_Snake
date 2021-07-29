import pygame
from datetime import datetime


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

while not done:
    for event in pygame.event.get():# User did something
        if event.type == pygame.QUIT:# If user clicked close
            done=True # Flag that we are done so we exit this loop
    block = pygame.Rect((2,2),(20,20))
    pygame.draw.rect(screen,WHITE,block)
    block = pygame.Rect((24,2),(20,20))
    pygame.draw.rect(screen,WHITE,block)
    block = pygame.Rect((46,2),(20,20))
    pygame.draw.rect(screen,WHITE,block)
    pygame.display.flip()
