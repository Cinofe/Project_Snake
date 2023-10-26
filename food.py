import random

class Food:
    def __init__(self):
        #색(빨강)
        self.foodColor = (255,0,0)
        #매번 좌표는 랜덤으로 부여
        self.pos = ((random.randint(0,29)*22)+4,(random.randint(0,29)*22)+6)
    
    def draw(self, env):
        env.draw_block(self.pos,self.foodColor)
    
    def relocation(self, snake):
        self.pos = ((random.randint(0,29)*22)+4,(random.randint(0,29)*22)+6)
        while self.pos in snake.positions:
            self.pos = ((random.randint(0,29)*22)+4,(random.randint(0,29)*22)+6)