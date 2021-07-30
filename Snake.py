import pygame
import time
import random
from datetime import datetime
from datetime import timedelta


#pygame 초기화
pygame.init()

#화면 크기
size = [850,668]

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

KEY_DIRECTION = {
    pygame.K_UP: 'U',
    pygame.K_DOWN: 'D',
    pygame.K_LEFT: 'L',
    pygame.K_RIGHT: 'R',
}

class Game_System:
     
    def draw_block(self, screen, color, position):
        block = pygame.Rect((position[0], position[1]), (20, 20))
        pygame.draw.rect(screen, color, block)


class Snake(Game_System):
    
    def __init__(self):
        self.positions = [(4,6),(26,6),(48,6)]
        self.direction = "D"

    def draw(self):
        for position in self.positions:
            super().draw_block(screen, WHITE, position)
    
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

class Apple(Game_System):
    def __init__(self,position = ((random.randint(0,30)*22)+4,(random.randint(0,30)*22)+6)):
        self.position = position
    def draw(self):
        super().draw_block(screen,RED,self.position)

snake = Snake()
apple = Apple()

while not done:
    clock.tick(60)
    screen.fill(BLACK)

    #테두리
    pygame.draw.rect(screen,WHITE,[0,2,664,666],2)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done=True
        if event.type == pygame.KEYDOWN:
            if event.key in KEY_DIRECTION:
                if KEY_DIRECTION[event.key] == "U" and snake.direction != 'D':
                    snake.direction = KEY_DIRECTION[event.key]
                elif KEY_DIRECTION[event.key] == "D" and snake.direction != 'U':
                    snake.direction = KEY_DIRECTION[event.key]
                elif KEY_DIRECTION[event.key] == "L" and snake.direction != 'R':
                    snake.direction = KEY_DIRECTION[event.key]
                elif KEY_DIRECTION[event.key] == "R" and snake.direction != 'L':
                    snake.direction = KEY_DIRECTION[event.key]
    
    if timedelta(seconds=0.075) <= datetime.now() - last_moved_time:
        snake.move()
        last_moved_time = datetime.now()

    if snake.positions[0] == apple.position:
        snake.grow()
        while True:
            new_position = ((random.randint(0,30)*22)+4,(random.randint(0,30)*22)+6)
            if not(new_position in snake.positions) and (new_position[0] >= 4 and new_position[0] < 664) and (new_position[1] >= 6 and new_position[1] < 666):
                apple.position = new_position
                break
            

    snake.draw()
    apple.draw()
    pygame.display.flip()
