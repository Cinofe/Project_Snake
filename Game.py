from datetime import datetime,timedelta
from gameEnv import Env
from snake import Snake
from dna import DNA
from neuralNet import NeuralNet
from food import Food
import pygame as pg

if __name__ == "__main__":
    env = Env()
    brain = NeuralNet(24,14,4)
    dna = DNA()
    #반복 횟수
    epoch = 500
    #모드 설정(0:ai, 1:user)
    mode = 1

    while epoch > 0:
        env.reset()
        snake = Snake()
        food = Food()
        # 매 반복마다 진화가 없다면 brain을 새로 생성
        if env.generation == 0:
            brain = NeuralNet(24,14,4)

        while True:
            #화면 구성 업데이트
            env.screenUpdate(snake, food, env)

            #종료 체크
            env.isDone(snake)
            if env.done:
                env.count += 1
                break
            
            #키보드 입력값 검사
            for event in pg.event.get():
                if event.type == pg.KEYDOWN:
                    #키보드 입력값 체크
                    if env.keyCheck(snake, event.key, mode=mode):
                        epoch = 0
                        break
            if timedelta(seconds=2) <= datetime.now() - env.last_moved_time2:
                env.score += 1
                env.last_moved_time2 = datetime.now()
            #second 는 한tick 즉 한 프레임당 시간을 말함 낮을 수록 뱀 이동속도 상승
            #현재 시간과 마지막 이동시간을 비교해서 0.5초 이상 지났을 경우 실행
            if timedelta(seconds=0.075) <= datetime.now() - env.last_moved_time:
                if mode == 0:
                    if env.isBest():
                        dna.append(brain, env)
                    #brain 반환 값 검사
                    if len(snake.food_Distance(food.pos)+snake.wall_Distance()+snake.body_Distance()) == 24:
                        result = brain.query(snake.food_Distance(food.pos)+snake.wall_Distance()+snake.body_Distance())
                        #이동 방향 설정
                        env.resultCheck(snake, result.index(max(result)))
                #뱀 이동
                snake.move()
                #이동 할 때 마다 남은 이동 수 감소
                env.life -= 1
                #마지막 이동시각 저장
                env.last_moved_time = datetime.now()
            
            #먹이 먹었는지 체크
            if snake.positions[0] == food.pos:
                snake.grow(env)
                food.relocation(snake)
        epoch -= 1