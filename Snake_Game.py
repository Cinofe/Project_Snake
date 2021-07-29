import pygame # 1. pygame 선언
import random
from datetime import datetime
from datetime import timedelta
 
pygame.init() # 2. pygame 초기화
 
# 3. pygame에 사용되는 전역변수 선언
WHITE = (255,255,255)
RED = (255,0,0)
BLACK = (0,0,0)
size = [600,620]
screen = pygame.display.set_mode(size)
 
done= False
clock= pygame.time.Clock()
last_moved_time = datetime.now()
 
KEY_DIRECTION = {
    pygame.K_UP: 'up',
    pygame.K_DOWN: 'down',
    pygame.K_LEFT: 'left',
    pygame.K_RIGHT: 'right',
}
 
def draw_block(screen, color, position):
    block = pygame.Rect((position[1] * 20, position[0] * 20),
                        (20, 20))
    pygame.draw.rect(screen, color, block)
 
class Snake:
    def __init__(self):
        self.positions = [(0,2),(0,1),(0,0)]  # 뱀의 위치
        self.direction = 'down'
 
    def draw(self):
        for position in self.positions: 
            draw_block(screen, WHITE, position)
 
    def move(self):
        head_position = self.positions[0]
        y, x = head_position
        if self.direction == 'up':
            self.positions = [(y - 1, x)] + self.positions[:-1]
        elif self.direction == 'down':
            self.positions = [(y + 1, x)] + self.positions[:-1]
        elif self.direction == 'left':
            self.positions = [(y, x - 1)] + self.positions[:-1]
        elif self.direction == 'right':
            self.positions = [(y, x + 1)] + self.positions[:-1]
 
    def grow(self):
        tail_position = self.positions[-1]
        y, x = tail_position
        if self.direction == 'up':
            self.positions.append((y - 1, x))
        elif self.direction == 'down':
            self.positions.append((y + 1, x))
        elif self.direction == 'left':
            self.positions.append((y, x - 1))
        elif self.direction == 'right':
            self.positions.append((y, x + 1))    
 
 
class Apple:
    def __init__(self, position=(5, 5)):
        self.position = position
 
    def draw(self):
        draw_block(screen, RED, self.position)
 
# 4. pygame 무한루프
def runGame():
    global done, last_moved_time
    #게임 시작 시, 뱀과 사과를 초기화
    snake = Snake() 
    apple = Apple()

    score = 0
    score_font = pygame.font.SysFont('OpenSans', 30)
 
    while not done:
        clock.tick(10)
        screen.fill(BLACK)
        snakeHead = snake.positions[0]
        
        pygame.draw.rect(screen,WHITE,[0,0,600,600],2)

        screen.blit(score_font.render("score : "+str(score),False,WHITE),(300,600))
 
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done=True
            if event.type == pygame.KEYDOWN:
                if event.key in KEY_DIRECTION:
                    if KEY_DIRECTION[event.key] == "up" and snake.direction != 'down':
                        snake.direction = KEY_DIRECTION[event.key]
                    elif KEY_DIRECTION[event.key] == "down" and snake.direction != 'up':
                        snake.direction = KEY_DIRECTION[event.key]
                    elif KEY_DIRECTION[event.key] == "left" and snake.direction != 'right':
                        snake.direction = KEY_DIRECTION[event.key]
                    elif KEY_DIRECTION[event.key] == "right" and snake.direction != 'left':
                        snake.direction = KEY_DIRECTION[event.key]

        if timedelta(seconds=0.1) <= datetime.now() - last_moved_time:
            snake.move()
            last_moved_time = datetime.now()
 
        if snake.positions[0] == apple.position:
            snake.grow()
            apple.position = (random.randint(0, 28), random.randint(0, 28))
            score += 10
        #자기 몸 충돌 종료
        if snake.positions[0] in snake.positions[1:]:
            done = True
        #벽 충돌 종료
        if snakeHead[1] < -1 or snakeHead[1] > 29 or snakeHead[0] < -1 or snakeHead[0] > 29:
            done = True
        print(f"x : {snakeHead[1]}, y : {snakeHead[0]}")
        
 
        snake.draw()
        apple.draw()
        pygame.display.update()
 
runGame()
pygame.quit()