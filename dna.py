import numpy as np, random, copy

class DNA:
    def __init__(self):
        self.clones = []
        self.scores = []
        self.parents = []
        self.count = 0
    #부모 선발
    def append(self, brain, env):
        #예비 부모가 10개체가 되면 선택
        if len(self.clones) < 10:
            self.clones.append(copy.deepcopy(brain))
            self.scores.append(env.score)
        elif len(self.clones) == 10:
            #룰렛 선택 방식으로 랜덤하게 선택
            s = sum(self.scores)
            #두 개체를 선정해야함으로 2번 반복
            for _ in range(2):
                ran = random.random() * s
                for i, j in enumerate(self.clones):
                    if ran > self.scores[i]:
                        ran -= self.scores[i]
                    else:
                        self.parents.append(self.clones[j])
                        break

            if random.randint(0,10000) <= 10:
                self.mutate()
            
            self.crossOver()
    #돌연변이
    def mutate(self):
        #선택된 부모중 2번째 개체에 돌연변이를 일으킴 1/1000 확률
        self.parents[1].Wi = np.random.uniform(-1,1,(self.parents[1].Wi.shape[0],self.parents[1].Wi.shape[1]))
        self.parents[1].Wh = np.random.uniform(-1,1,(self.parents[1].Wh.shape[0],self.parents[1].Wh.shape[1]))
        self.parents[1].Wo = np.random.uniform(-1,1,(self.parents[1].Wo.shape[0],self.parents[1].Wo.shape[1]))
    #합성
    def crossOver(self, env):
        pass
        env.generation += 1

